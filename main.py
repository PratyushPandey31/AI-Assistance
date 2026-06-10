from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "pratyush_secret_fallback_key_2026")

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
gemini_key = os.getenv("GEMINI_API_KEY")

# SQLite Configuration (uses /tmp on Vercel to allow writes)
DATABASE = "/tmp/users.db" if os.environ.get("VERCEL") else "users.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db_dir = os.path.dirname(DATABASE)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
    conn = get_db_connection()
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

# Initialize Database
init_db()

client = None
provider = None
model_name = None

# Configure API client based on available keys
if gemini_key and len(gemini_key.strip()) > 5:
    try:
        provider = "Gemini"
        model_name = "gemini-3.5-flash"
        client = OpenAI(
            api_key=gemini_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
        print(f"Configured Gemini API using model {model_name}")
    except Exception as e:
        print(f"Error configuring Gemini: {e}")
        client = None
elif openai_key and len(openai_key.strip()) > 10:
    try:
        provider = "OpenAI"
        model_name = "gpt-4o"
        client = OpenAI(api_key=openai_key)
        print(f"Configured OpenAI API using model {model_name}")
    except Exception as e:
        print(f"Error configuring OpenAI: {e}")
        client = None

is_api_configured = client is not None

@app.route("/")
def hello_world():
    if "user_id" not in session:
        return redirect(url_for("login_page"))
    return render_template("index.html", is_simulated=not is_api_configured, provider=provider, username=session.get("username"))

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if "user_id" in session:
        return redirect(url_for("hello_world"))
        
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()
        
        if not username or not password:
            flash("Please fill in all fields.", "error")
            return render_template("login.html")
            
        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user["password_hash"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("hello_world"))
        else:
            flash("Invalid username or password.", "error")
            
    return render_template("login.html")

@app.route("/signup", methods=["POST"])
def signup_action():
    if "user_id" in session:
        return redirect(url_for("hello_world"))
        
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()
    
    if not username or not password:
        flash("Please fill in all fields.", "error")
        return redirect(url_for("login_page"))
        
    if len(password) < 6:
        flash("Password must be at least 6 characters.", "error")
        return redirect(url_for("login_page"))
        
    conn = get_db_connection()
    try:
        password_hash = generate_password_hash(password)
        conn.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        flash("Signup successful! Please log in.", "success")
    except sqlite3.IntegrityError:
        flash("Username already exists.", "error")
    finally:
        conn.close()
        
    return redirect(url_for("login_page"))

@app.route("/logout")
def logout_action():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login_page"))

@app.route("/ask", methods=["POST"])
def ask():
    if "user_id" not in session:
        return jsonify({"response": "Unauthorized access. Please log in first."}), 401
        
    question = request.form.get("question", "").strip()
    if not question:
        return jsonify({"response": "Please ask a valid question."}), 400
    
    if is_api_configured and client:
        try:
            if provider == "Gemini":
                # Call Gemini via OpenAI compatibility interface
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "Act like a helpful personal assistant"},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.7,
                    max_tokens=800
                )
                answer = response.choices[0].message.content.strip()
                return jsonify({"response": answer}), 200
            
            else: # OpenAI
                try:
                    # Try original responses API (gpt-5.4)
                    response = client.responses.create(
                        model="gpt-5.4",
                        input=[
                            {"role": "system", "content": "Act like a helpful personal assistant"},
                            {"role": "user", "content": question}
                        ],
                        temperature=0.7,
                        max_output_tokens=512
                    )
                    answer = response.output_text.strip()
                    return jsonify({"response": answer}), 200
                except Exception as e:
                    print(f"Error with Responses API (gpt-5.4): {e}. Trying ChatCompletions fallback...")
                    # Try fallback standard chat completions (gpt-4o)
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "Act like a helpful personal assistant"},
                            {"role": "user", "content": question}
                        ],
                        temperature=0.7,
                        max_tokens=512
                    )
                    answer = response.choices[0].message.content.strip()
                    return jsonify({"response": answer}), 200
                    
        except Exception as ex:
            print(f"API Error: {ex}. Falling back to simulation.")
            return jsonify({
                "response": f"[Simulation Mode - API Error: {ex}]\n\nI received your question: \"{question}\". Since the API call failed, here is a simulated response. Please verify your API key validity."
            }), 200
    else:
        # Simulation Mode
        simulated_response = (
            f"🤖 [Simulation Mode]\n\n"
            f"You asked: \"{question}\"\n\n"
            f"If an API key was configured, this response would be generated dynamically "
            f"using {model_name or 'AI models'}. For now, here is a simulated answer: Your Flask application is fully configured "
            f"and running. You can ask questions, manage data, and summarize text once a valid API key is set!"
        )
        return jsonify({"response": simulated_response}), 200

@app.route("/summarize", methods=["POST"])
def summarize():
    if "user_id" not in session:
        return jsonify({"response": "Unauthorized access. Please log in first."}), 401
        
    email_text = request.form.get("email", "").strip()
    if not email_text:
        return jsonify({"response": "Please provide email text to summarize."}), 400
        
    prompt = f"summarize the following email in 2-3 sentences:\n\n{email_text}"
    
    if is_api_configured and client:
        try:
            if provider == "Gemini":
                # Call Gemini via OpenAI compatibility interface
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": "Act like an expert email assistant"},                
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    max_tokens=800
                )
                summary = response.choices[0].message.content.strip()
                return jsonify({"response": summary}), 200
            
            else: # OpenAI
                try:
                    response = client.responses.create(
                        model="gpt-5.4",
                        input=[
                            {"role": "system", "content": "Act like an expert email assistant"},                
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.3,
                        max_output_tokens=512
                    )
                    summary = response.output_text.strip()
                    return jsonify({"response": summary}), 200
                except Exception as e:
                    print(f"Error with Responses API (gpt-5.4): {e}. Trying ChatCompletions fallback...")
                    response = client.chat.completions.create(
                        model=model_name,
                        messages=[
                            {"role": "system", "content": "Act like an expert email assistant"},                
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.3,
                        max_tokens=512
                    )
                    summary = response.choices[0].message.content.strip()
                    return jsonify({"response": summary}), 200
                    
        except Exception as ex:
            print(f"API Error: {ex}. Falling back to simulation.")
            return jsonify({
                "response": f"[Simulation Mode - API Error: {ex}]\n\nEmail Summary Simulation: The email details discussions regarding key action items. To see a real AI summary, please check your API key."
            }), 200
    else:
        # Simulation Mode: Parse the email to make the summary look smart
        lines = [line.strip() for line in email_text.split("\n") if line.strip()]
        subject = "No Subject"
        sender = "Unknown Sender"
        for line in lines[:5]:
            if line.lower().startswith("subject:"):
                subject = line[8:].strip()
            elif line.lower().startswith("from:"):
                sender = line[5:].strip()
        
        body_snippet = " ".join(lines[:3])
        if len(body_snippet) > 120:
            body_snippet = body_snippet[:120] + "..."
            
        simulated_summary = (
            f"📧 [Simulation Mode Summary]\n\n"
            f"• Sender/Context: {sender if sender != 'Unknown Sender' else 'Parsed from message body'}\n"
            f"• Main Subject: {subject if subject != 'No Subject' else 'General correspondence'}\n"
            f"• Content Summary: The email outlines key points stating: \"{body_snippet}\". "
            f"To get a real AI-generated summary, add a valid API key."
        )
        return jsonify({"response": simulated_summary}), 200

if __name__ == "__main__":
    app.run(debug=True)




