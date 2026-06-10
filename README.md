# AI CoPilot: Flask-Powered Assistant & Email Summarization Tool

A highly responsive, visually stunning web application built on Flask that integrates Google's **Gemini 3.5 Flash** models (via OpenAI compatibility) to answer user questions and generate neat summaries of long emails.

## 🚀 Live Deployment

The application is deployed and live on Vercel:
👉 **[https://pratyush-ai-assistance.vercel.app](https://pratyush-ai-assistance.vercel.app)**

---

## ✨ Features

- **Ask Anything**: Enter your question and receive instant, intelligent responses powered by Gemini.
- **Email Summarization**: Input the text of any email and get a concise 2-3 sentence overview highlighting sender, subject, and core context.
- **Dual Mode Support**:
  - **Live API Mode**: Connects directly to the Gemini API using the key configured in environment variables.
  - **Simulation Mode**: A robust mock fallback that allows users to test interface features and view simulated outputs even if no API key is set.
- **Premium Glassmorphic Design**:
  - Floating ambient gradient orbs creating visual depth.
  - A responsive two-column grid separating controls into color-accented panels (Cyan for general questions, Purple for email summarization).
  - Modern typography (`Outfit` from Google Fonts).
  - High fidelity inputs, loaders, and transitions.

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask, `python-dotenv`
- **Frontend**: HTML5, Vanilla CSS3 (Custom Grid, Animations, Variables)
- **AI Engine**: `openai` SDK mapped to Google's Gemini OpenAI-compatibility gateway (`gemini-3.5-flash`)
- **Hosting**: Vercel Serverless (Python)

---

## 💻 Local Setup & Execution

Follow these steps to run the application locally on your computer:

### 1. Clone the repository
```bash
git clone https://github.com/PratyushPandey31/AI-Assistance.git
cd AI-Assistance
```

### 2. Create and activate a Virtual Environment
On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```
On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a file named `.env` in the root directory and add your API key:
```env
GEMINI_API_KEY=your-actual-gemini-api-key
```

### 5. Start the server
```bash
python main.py
```
Open **[http://127.0.0.1:5000](http://127.0.0.1:5000)** in your browser to view the app!

---

## 🔒 Security & Safe Committing

All configuration files (`.env`), local environments (`venv/`), and compilation caches are ignored by Git in `.gitignore` to prevent any credential leaks or junk commits.