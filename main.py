from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import bcrypt

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load Env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

import models
from database import SessionLocal, engine, get_db
from questions_data import questions

# Create Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="NextStep")

# Mount Static & Templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto"]) # Removed

def verify_password(plain_password, hashed_password):
    # Ensure bytes for bcrypt
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def get_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return None
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    return user

# Routes

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if user:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check existing user
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Email already exists"})
    
    # Create User
    hashed_pw = get_password_hash(password)
    new_user = models.User(email=email, hashed_password=hashed_pw, full_name=full_name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Login & Redirect
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=str(new_user.id))
    return response

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...), # OAuth2PasswordRequestForm uses 'username' for email often, but standard form can be 'email'
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == username).first()
    if not user or not verify_password(password, user.hashed_password):
         return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=str(user.id))
    return response

@app.get("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("user_id")
    return response

@app.get("/login/google")
async def login_google(request: Request, db: Session = Depends(get_db)):
    # Mock Google Login
    email = "student@gmail.com"
    user = db.query(models.User).filter(models.User.email == email).first()
    
    if not user:
        # Create Google User if not exists
        hashed_pw = get_password_hash("google_demo_pass")
        user = models.User(email=email, hashed_password=hashed_pw, full_name="Google Student")
        db.add(user)
        db.commit()
        db.refresh(user)
    
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="user_id", value=str(user.id))
    return response

# --- Assessment Data ---

QUESTIONS = [
    {
        "id": "Q1_SocialBattery",
        "title": "Social Battery",
        "options": [
            {"value": "A", "text": "A quiet morning with a book/coffee.", "image": "/static/images/assessment/q1_social_battery_a.png"},
            {"value": "B", "text": "A high-energy concert with a crowd.", "image": "/static/images/assessment/q1_social_battery_b.png"}
        ]
    },
    {
        "id": "Q2_Communication",
        "title": "Communication",
        "options": [
            {"value": "A", "text": "Sending a carefully crafted email.", "image": "/static/images/assessment/q2_communication_a.png"},
            {"value": "B", "text": "Hopping on a quick, 'face-to-face' video call.", "image": "/static/images/assessment/q2_communication_b.png"}
        ]
    },
    {
        "id": "Q3_Workspace",
        "title": "Workspace",
        "options": [
            {"value": "A", "text": "A private pod with noise-canceling headphones.", "image": "/static/images/assessment/q3_workspace_a.png"},
            {"value": "B", "text": "A bustling co-working space with open desks.", "image": "/static/images/assessment/q3_workspace_b.png"}
        ]
    },
    {
        "id": "Q4_ProblemSolving",
        "title": "Problem Solving",
        "options": [
            {"value": "A", "text": "Digging through Google/Manuals solo.", "image": "/static/images/assessment/q4_problem_solving_a.png"},
            {"value": "B", "text": "Bouncing ideas off a group on a whiteboard.", "image": "/static/images/assessment/q4_problem_solving_b.png"}
        ]
    },
    {
        "id": "Q5_MeetingRole",
        "title": "Meeting Role",
        "options": [
            {"value": "A", "text": "The person taking detailed, silent notes.", "image": "/static/images/assessment/q5_meeting_role_a.png"},
            {"value": "B", "text": "The person leading the brainstorm out loud.", "image": "/static/images/assessment/q5_meeting_role_b.png"}
        ]
    },
     {
        "id": "Q6_LearningStyle",
        "title": "Learning Style",
        "options": [
            {"value": "A", "text": "Watching a deep-dive documentary alone.", "image": "/static/images/assessment/q6_learning_style_a.png"},
            {"value": "B", "text": "Attending a live, interactive workshop.", "image": "/static/images/assessment/q6_learning_style_b.png"}
        ]
    },
    {
        "id": "Q7_GoalPath",
        "title": "Goal: Path",
        "options": [
            {"value": "A", "text": "A straight highway with a clear destination.", "image": "/static/images/assessment/q7_goal_path_a.png"},
            {"value": "B", "text": "A winding trail through a beautiful forest.", "image": "/static/images/assessment/q7_goal_path_b.png"}
        ]
    },
    {
        "id": "Q8_GoalVision",
        "title": "Goal: Vision",
        "options": [
            {"value": "A", "text": "I have a 'Dream Job' title in my head.", "image": "/static/images/assessment/q8_goal_vision_a.png"},
            {"value": "B", "text": "I have a 'Lifestyle' I want, but the job is tbd.", "image": "/static/images/assessment/q8_goal_vision_b.png"}
        ]
    },
    {
        "id": "Q9_GoalSpeed",
        "title": "Goal: Speed",
        "options": [
            {"value": "A", "text": "I want to specialize and be the best at one thing.", "image": "/static/images/assessment/q9_goal_speed_a.png"},
            {"value": "B", "text": "I want to be a 'Jack of all trades' and know a bit of everything.", "image": "/static/images/assessment/q9_goal_speed_b.png"}
        ]
    },
    {
        "id": "Q10_GoalChoice",
        "title": "Goal: Choice",
        "options": [
            {"value": "A", "text": "I’d pick the 'Safe & Known' successful path.", "image": "/static/images/assessment/q10_goal_choice_a.png"},
            {"value": "B", "text": "I’d pick the 'Wildcard' path with high potential.", "image": "/static/images/assessment/q10_goal_choice_b.png"}
        ]
    }
]

# --- Assessment Routes ---

@app.get("/assessment", response_class=HTMLResponse)
async def assessment_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("assessment.html", {"request": request, "user": user, "questions": QUESTIONS})

@app.post("/assessment/submit")
async def assessment_submit(
    request: Request,
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    # 1. Collect Answers & Map to Text
    form_data = await request.form()
    user_answers_data = {}
    
    # helper map
    questions_map = {q["id"]: q for q in questions}

    for key, value in form_data.items():
        if key in questions_map:
            q_data = questions_map[key]
            # Find the selected option text
            selected_option = next((opt for opt in q_data["options"] if opt["value"] == value), None)
            if selected_option:
                user_answers_data[key] = selected_option["text"]
            else:
                 user_answers_data[key] = value # Fallback
        else:
             user_answers_data[key] = value

    # 2. Construct Prompt
    prompt = f"""
    You are an expert student career psychologist.

    Your task:
    1. Identify the user's Personality Type based on Q1–Q6:
       - Introvert
       - Ambivert
       - Extrovert

    2. Identify Goal Status based on Q7–Q10:
       - Goal Aware
       - Exploring

    3. Combine them into ONE of these 6 categories (Phase 2 Category):
       - Focused Specialist
       - Quiet Explorer
       - Strategic Builder
       - Adaptive Explorer
       - Visionary Leader
       - Dynamic Generalist

    Rules:
    - Do NOT invent traits.
    - Use majority patterns, but handle mixed answers intelligently.
    - Output must be VALID JSON only. Do not include markdown formatting like ```json.
    
    Structure:
    {{
      "personality": "String",
      "goal_status": "String",
      "phase_2_category": "String",
      "confidence": Float (0.0-1.0),
      "reasoning": "String (2-3 sentences max)"
    }}

    User Answers (Text Descriptions of Visual Choices):
    {json.dumps(user_answers_data, indent=2)}
    """

    # 3. Call Gemini
    if not GEMINI_API_KEY:
        # Fallback Mock for Demo if Key Missing
        result_data = {
            "personality": "Ambivert",
            "goal_status": "Exploring",
            "phase_2_category": "Adaptive Explorer",
            "confidence": 0.85,
            "reasoning": "Demo Mode: API Key missing. You showed balanced traits."
        }
    else:
        try:
            model = genai.GenerativeModel("gemini-flash-latest")
            response = model.generate_content(prompt)
            # Clean response text (sometimes models output markdown blocks)
            clean_text = response.text.replace("```json", "").replace("```", "").strip()
            result_data = json.loads(clean_text)
        except Exception as e:
            print(f"Gemini Error: {e}")
            result_data = {
                 "personality": "Error",
                 "goal_status": "Error",
                 "phase_2_category": "System Error",
                 "confidence": 0.0,
                 "reasoning": "Could not process assessment at this time."
            }

    # 4. Save to DB
    # Check if exists (overwrite for MVP simplicity)
    existing = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    if existing:
        db.delete(existing)
        db.commit()

    new_result = models.AssessmentResult(
        user_id=user.id,
        phase_2_category=result_data.get("phase_2_category"),
        personality=result_data.get("personality"),
        goal_status=result_data.get("goal_status"),
        confidence=result_data.get("confidence"),
        reasoning=result_data.get("reasoning"),
        raw_answers=user_answers_data
    )
    db.add(new_result)
    db.commit()

    return RedirectResponse(url="/assessment/result", status_code=status.HTTP_302_FOUND)

@app.get("/assessment/result", response_class=HTMLResponse)
async def assessment_result(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    result = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    if not result:
        return RedirectResponse(url="/assessment", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("result.html", {"request": request, "user": user, "result": result})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Fetch assessment result to show on dashboard
    assessment = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user, "assessment": assessment})

@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    # 1. Check if user is logged in
    user = get_current_user(request, db)
    if not user:
         return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    # 2. Fetch all users with their assessment results
    # Using 'joinedload' strategy via relationship is best, but since relationship is defined, standard query works.
    # However, to avoid N+1 problem, ideally we'd eager load, but for MVP separate queries or relationship loading is fine.
    # SQLAlchemy default lazy loading will work as we iterate in template.
    all_users = db.query(models.User).all()
    
    return templates.TemplateResponse("admin_dashboard.html", {"request": request, "user": user, "users": all_users})

