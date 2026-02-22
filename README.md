


<p align="center">
  <img src="Screenshot 2026-02-22 at 10.31.30 PM.png" alt="NEXTSTEP Logo" width="200"/>
</p>

# NEXTSTEP

An AI-powered career assessment and guidance platform built with FastAPI. Designed for students (Class 10th, 12th, and Above) to discover their personality archetype, explore career streams, and get personalized guidance through a multi-phase assessment and an AI chatbot.

---

## Features

- **Multi-Phase Assessment**: 4-phase structured assessment pipeline:
  - **Phase 1** – Class/Grade Selection (10th, 12th, Above 12th)
  - **Phase 2** – AI Personality Archetype Quiz (10 visual questions → 6 archetypes)
  - **Phase 3** – In-depth Scenario Analysis tailored to the user's archetype
  - **Phase 4** – Final Stream/Career Assessment with AI-powered recommendations
- **AI-Powered Analysis**: Dual AI provider system using **Google Gemini** (primary) with automatic fallback to **Groq (Llama 3.3-70B)**
- **AI Career Chatbot**: Personalized career counseling chatbot (`NextStep AI`) with token-by-token streaming and conversation history
- **User Authentication**: Secure signup/login with bcrypt password hashing and cookie-based sessions
- **Google Sign-In**: Mock Google OAuth login for quick demo access
- **Admin Dashboard**: View all users and their assessment results; delete users
- **Result Tracking**: Detailed result page with stream scores, pros/cons, and AI analysis tailored by grade level
- **SQLite Database**: Persistent storage with SQLAlchemy ORM; migration scripts included

---

## System Architecture

![System Architecture](Student-Centric%20Async%20API-2026-02-18-131456.png)

---

## Tech Stack

| Layer      | Technology                                     |
|------------|------------------------------------------------|
| Backend    | FastAPI, Uvicorn                               |
| Templating | Jinja2                                         |
| Database   | SQLite + SQLAlchemy ORM                        |
| AI (Primary) | Google Gemini (`gemini-flash-latest`)        |
| AI (Fallback) | Groq API (`llama-3.3-70b-versatile`)        |
| Auth       | bcrypt, Cookie-based sessions                  |
| Frontend   | HTML, CSS, JavaScript (served via Jinja2)      |
| Config     | python-dotenv                                  |

---

## Project Structure

```
NEXTSTEP/
├── app/                          # Main application package
│   ├── __init__.py
│   ├── main.py                   # FastAPI app, all routes & AI logic
│   ├── models.py                 # SQLAlchemy database models
│   ├── database.py               # DB engine, session, and base
│   ├── static/                   # Static files (images, CSS, JS)
│   │   └── images/
│   │       └── assessment/       # Assessment option images (q1_a.png, etc.)
│   └── templates/                # Jinja2 HTML templates
│       ├── base.html
│       ├── login.html
│       ├── signup.html
│       ├── dashboard.html
│       ├── admin_dashboard.html
│       ├── assessment.html       # Phase 2: Archetype quiz
│       ├── assessment_phase3.html# Phase 3: Scenario deep-dive
│       ├── assessment_final.html # Phase 4: Stream/career assessment
│       ├── chatbot.html          # AI career chatbot
│       └── result.html           # Final results with AI analysis
├── data/                         # Question data modules
│   ├── __init__.py
│   ├── questions_data.py         # Phase 2 archetype questions
│   ├── questions_phase3.py       # Phase 3 scenario map (by archetype)
│   ├── questions_final.py        # Phase 4 questions (Class 10: 4 sections)
│   ├── questions_12th.py         # Phase 4 questions for Class 12th
│   └── questions_above_12th.py   # Phase 4 questions for Above 12th
├── scripts/                      # Utility scripts
│   ├── list_users.py             # List all registered users
│   ├── manage_test_data.py       # Seed/clean test data
│   ├── migrate_db_v2.py          # DB schema migration v2
│   ├── migrate_db_v5.py          # DB schema migration v5
│   ├── rename_images.py          # Rename assessment images
│   └── verify_classification.py  # Verify AI category classification
├── learnloop.db                  # SQLite database file
├── requirements.txt              # Python dependencies
├── run.py                        # Application entry point
└── README.md                     # This file
```

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Yuvneet22/NEXTSTEP.git
cd NEXTSTEP
```

### 2. Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```env
GEMINI_API_KEY=your-gemini-api-key-here
GROQ_API_KEY=your-groq-api-key-here
```

- Get your **Gemini API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Get your **Groq API key** from [Groq Console](https://console.groq.com)

> **Note**: The app works without API keys in demo mode, but AI analysis and chatbot responses will be mocked.

### 5. Run the application
```bash
python run.py
```

The app will be available at: **`http://127.0.0.1:8000`**

API docs (Swagger UI): **`http://127.0.0.1:8000/docs`**

---

## Usage

### Student Flow

| Step | Route | Description |
|------|-------|-------------|
| Signup | `/signup` | Create a new student account |
| Login | `/login` | Login with email & password |
| Google Login | `/login/google` | Quick mock Google Sign-In |
| Dashboard | `/dashboard` | View assessment summary and progress |
| Phase 1 | `/assessment/start?class_level=10th` | Select class level (10th / 12th / Above 12th) |
| Phase 2 | `/assessment` | 10-question visual archetype quiz |
| Phase 3 | `/assessment/phase3` | Scenario deep-dive based on archetype |
| Phase 4 | `/assessment/final` | Stream/career assessment |
| Results | `/assessment/result` | Full AI-powered result report |
| Chatbot | `/chatbot` | Chat with NextStep AI for career guidance |

### Admin Flow

| Route | Description |
|-------|-------------|
| `/admin` | View all users and their assessment results |
| `/admin/users/{id}/delete` | Delete a user and their data |

---

## Assessment Pipeline

```
Phase 1 ──► Phase 2 ──────────────────► Phase 3 ──────────────► Phase 4
(Class)     (10 Visual Q → Archetype)   (Scenario Analysis)     (Stream/Career)
                    │                           │                       │
                    ▼                           ▼                       ▼
              Google Gemini           Gemini / Groq Fallback    Gemini / Groq Fallback
              Classification         Work Style Analysis        Stream + AI Report
```

**6 Personality Archetypes**: Focused Specialist, Quiet Explorer, Strategic Builder, Adaptive Explorer, Visionary Leader, Dynamic Generalist

**Class 10 Streams**: Science (PCM), Science (PCB), Commerce, Arts & Humanities, Vocational Studies

**Class 12 / Above 12th**: Top 3 career paths / professional roles identified by AI

---

## Database Models

| Model | Key Fields |
|-------|-----------|
| `User` | `id`, `email`, `hashed_password`, `full_name`, `role` |
| `AssessmentResult` | `selected_class`, `phase_2_category`, `personality`, `goal_status`, `phase3_analysis`, `recommended_stream`, `final_analysis`, `stream_pros`, `stream_cons` |
| `ChatMessage` | `user_id`, `sender` (`user`/`ai`), `content`, `timestamp` |

---

## Utility Scripts

Run from the project root:

```bash
# List all registered users
python scripts/list_users.py

# Seed or clean test data
python scripts/manage_test_data.py

# Run database migration (v2)
python scripts/migrate_db_v2.py

# Run database migration (v5)
python scripts/migrate_db_v5.py

# Verify AI classification output
python scripts/verify_classification.py

# Rename assessment images
python scripts/rename_images.py
```

---

## AI Fallback Strategy

The app uses a **dual-provider AI system** to maximize uptime:

1. **Primary**: Google Gemini (`gemini-flash-latest`) — classification, analysis, chatbot
2. **Fallback**: Groq API (`llama-3.3-70b-versatile`) — activates if Gemini call fails

All AI responses are cleaned with robust JSON extraction (handles markdown blocks, trailing commas, etc.)

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
