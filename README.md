# KAVACH AI 🛡️
### AI-Powered Digital Brand Protection & Impersonation Monitoring

## 📌 Project Overview

KAVACH AI is a digital brand protection platform designed to help identify potential fake profiles, impersonation accounts, suspicious mobile apps, and online threats targeting brands.

The platform provides a dashboard to register brand details, review potential risks, and monitor available data sources.

## 🎯 Problem Statement

Brands face online threats such as fake social media profiles, fraudulent apps, and impersonation attempts. Manually identifying these threats across multiple platforms can be difficult and time-consuming.

KAVACH AI aims to simplify brand monitoring through a centralized dashboard.

## ✨ Key Features

- **Brand Profile Management:** Register brand names, official websites, social media handles, and app details.
- **Social Media Monitoring:** Review potential impersonation profiles and suspicious accounts.
- **App Monitoring:** Organize and assess potential fake or suspicious mobile applications.
- **Auto Discovery:** Explore potential brand-related accounts and findings.
- **Threat Dashboard:** View registered brands, assessed candidates, cases requiring review, and resolved cases.
- **Backend Integration:** Connect the dashboard to a Python FastAPI backend.
- **Integration Status:** View API verification and demo-mode status for supported platforms.

## 🛠️ Technology Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python, FastAPI
- **Server:** Uvicorn
- **External Data Sources:** YouTube Data API, Apple iTunes Lookup API, and Bluesky public search, subject to configuration and availability.
- **Frontend Deployment:** Vercel
- **Backend Deployment:** Render
- **Version Control:** Git and GitHub

## 🌐 Live Demo

- **Frontend:** https://kavach-ai-nine-sandy.vercel.app/
- **Backend:** https://kavach-ai-yi5a.onrender.com/

## 🚀 Local Setup Instructions

### Prerequisites

- Python 3.10 or later
- pip
- A web browser

### 1. Clone the repository

```bash
git clone https://github.com/Nikhil018-Yelisetti/Kavach-AI.git
cd Kavach-AI
```

### 2. Install backend dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file inside the `backend` directory for any required API credentials.

Never upload API keys, access tokens, or passwords to GitHub.

### 4. Start the backend

Run this command from the `backend` directory:

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

The backend should be available at:

`http://127.0.0.1:8000`

FastAPI documentation, if enabled, is available at:

`http://127.0.0.1:8000/docs`

### 5. Open the frontend

Open `index.html` in a web browser. In API Settings, enter the backend URL and save it.

For local testing, use:

`http://127.0.0.1:8000`

For the deployed application, use the deployed backend URL listed above.

## 🔍 How It Works

1. Register a brand and its official details.
2. Configure the backend connection.
3. Run a sample scan or a backend scan.
4. Review potential findings in the dashboard.
5. Examine suspicious candidates and investigate cases.

## ⚠️ Current Limitations

- Some platforms operate in demo mode and are not connected to live APIs.
- Live monitoring depends on API access, permissions, and service availability.
- Scan findings require verification; demo results must not be treated as confirmed threats.
- The prototype does not guarantee detection of every impersonation attempt.

## 🔮 Future Enhancements

- Integrate additional authorized social media and app-store APIs.
- Improve suspicious account detection using machine learning.
- Add automated alerts and notifications.
- Expand threat investigation and reporting features.

## 👥 Team

**Project Name:** KAVACH AI  
**Category:** Digital Risk Protection  
**Repository:** [Kavach-AI on GitHub](https://github.com/Nikhil018-Yelisetti/Kavach-AI)

## 📄 License

This project was developed as a hackathon prototype. Licensing and third-party API usage must comply with the relevant platform terms.
