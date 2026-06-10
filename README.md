# 🤖 AI CoPilot: Intelligent Assistant & Email Summarizer

<p align="center">
  <img src="https://img.shields.io/badge/Vercel-Deployed-success?style=for-the-badge&logo=vercel&logoColor=white&color=000000" alt="Vercel Deploy" />
  <img src="https://img.shields.io/badge/Gemini-Powered-blue?style=for-the-badge&logo=google-gemini&logoColor=white&color=1A73E8" alt="Gemini Powered" />
  <img src="https://img.shields.io/badge/Flask-v3.1.3-orange?style=for-the-badge&logo=flask&logoColor=white&color=000000" alt="Flask version" />
  <img src="https://img.shields.io/badge/Python-v3.10+-blue?style=for-the-badge&logo=python&logoColor=white&color=3776AB" alt="Python Version" />
</p>

---

## 🔗 Live Demo
Experience the live, responsive web app deployed on Vercel:
👉 **[https://pratyush-ai-assistance.vercel.app](https://pratyush-ai-assistance.vercel.app)**

---

## 📝 Project Overview

**AI CoPilot** is a modern, lightweight, and visually stunning web application built on **Flask** that serves as a personal virtual assistant. It leverages Google's state-of-the-art **Gemini 3.5 Flash** models to perform two major workflows:
1. **Interactive Assistant**: Answer general queries dynamically with high-context accuracy.
2. **Email Summarization**: Parse lengthy, cluttered emails and generate clean, bulleted summaries containing the sender name, core subject, and critical action points.

The interface is redesigned from the ground up to follow **Premium Glassmorphic Design Aesthetics**—featuring ambient neon glow effects, responsive card grids, and high-fidelity loading states.

---

## ✨ Key Features

### 🧠 Gemini 3.5 Flash Integration
- Fully integrated with Google's latest generative models using the OpenAI-compatible endpoint.
- Optimized response caching and system prompts for high-speed delivery.

### 🛡️ Smart Simulation Fallback (Fail-Safe)
- If the API key is missing or calls fail due to quota limit restrictions, the backend automatically transitions to **Simulation Mode**.
- Generates smart, parsed mock answers instead of breaking the UI, providing a seamless demonstration out of the box.

### 🎨 Premium Glassmorphic User Interface
- **Ambient Glow Orbs**: Floating cyan and purple background light sources that move dynamically in the background.
- **Two-Column Responsive Grid**: Separates workflows into visual modules (Cyan-themed Q&A, Purple-themed Email Summarization).
- **Responsive Design**: Stacks vertically on mobile screens and presents a clean dashboard layout on desktops.
- **Micro-Animations**: Hover animations on cards, neon focus states on text inputs, and custom CSS loaders.

---

## 📁 Repository Directory Structure

```text
AI-Assistance/
│
├── static/
│   └── style.css       # Core stylesheet (dark glassmorphism, responsive grid, animations)
│
├── templates/
│   └── index.html      # Responsive dashboard UI (status indicators, SVG icons, forms)
│
├── .env                # Local configuration (API Keys - Git-ignored)
├── .gitignore          # Safeguards virtual envs, secrets, and Vercel build configs
├── main.py             # Main Flask server (handles routing, multi-provider API setup, and simulation logic)
├── requirements.txt    # Lists all required Python packages for deployment
└── vercel.json         # Vercel Serverless Function routing and build configuration
```

---

## 💻 Local Setup & Installation

Follow this step-by-step guide to run the project locally on your machine:

### 1. Clone the Repository
```bash
git clone https://github.com/PratyushPandey31/AI-Assistance.git
cd AI-Assistance
```

### 2. Set Up a Virtual Environment (Recommended)
This isolates the project dependencies so they do not conflict with your global Python setup.

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key
Create a `.env` file in the root directory:
```bash
touch .env
```
Open `.env` in your code editor and add your Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key
```

### 5. Launch the Local Server
```bash
python main.py
```
Open your web browser and go to:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 🌐 Production Deployment

The project is configured to run serverless on Vercel. 

### Deployment configuration (`vercel.json`)
The application is mapped using Vercel's Python runtime (`@vercel/python`):
```json
{
  "version": 2,
  "builds": [
    {
      "src": "main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "main.py"
    }
  ]
}
```

### How to Deploy Your Own:
1. Install Vercel CLI: `npm install -g vercel`
2. Link your Vercel account: `vercel login`
3. Deploy to production while passing your environment variables:
   ```bash
   vercel --name pratyush-ai-assistance -e GEMINI_API_KEY=your_key --prod --yes
   ```