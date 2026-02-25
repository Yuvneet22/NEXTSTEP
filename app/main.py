from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, Response
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import bcrypt

import os
import json
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv
from starlette.middleware.sessions import SessionMiddleware
from authlib.integrations.starlette_client import OAuth

# Load Env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None

# OAuth Setup
oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

def generate_content_with_fallback(prompt):
    """
    Attempts to generate content using Gemini.
    Falls back to Groq (Llama 3) if Gemini fails.
    Returns cleaned text (JSON-ready).
    """
    try:
        # Try Gemini First
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(prompt)
        text = response.text
    except Exception as e:
        print(f"Gemini Error (Switching to Groq): {e}")
        if not groq_client:
            raise e # No fallback available
        
        try:
            # Fallback to Groq
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama-3.3-70b-versatile",
            )
            text = chat_completion.choices[0].message.content
        except Exception as groq_e:
            raise Exception(f"Both APIs failed. Gemini: {e}, Groq: {groq_e}")

    # Robust JSON Extraction
    import re
    try:
        # Find JSON object between first { and last }
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            text = match.group(0)
        
        # Remove markdown code blocks if still present
        text = text.replace("```json", "").replace("```", "").strip()
        
        # Remove trailing commas
        text = re.sub(r",\s*([\]}])", r"\1", text)
        
        return text
    except Exception:
        return text # Return original if extraction fails, let json.loads raise the error

from . import models
from .database import SessionLocal, engine, get_db
from data.questions_data import questions
from data.questions_12th import questions_12th
from data.questions_above_12th import questions_above_12th

# Create Tables - Enabled for local development
# models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="NextStep")

# Add Session Middleware (needed for OAuth)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "a_very_secret_key_for_sessions"))

# Mount Static & Templates
# Mount Static & Templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
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
    contact_number: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check existing user
    user = db.query(models.User).filter(models.User.email == email).first()
    if user:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Email already exists"})
    
    # Create User
    hashed_pw = get_password_hash(password)
    new_user = models.User(email=email, hashed_password=hashed_pw, full_name=full_name, contact_number=contact_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Login & Redirect
    # Redirect to Login (No auto-login)
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()
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
async def login_google(request: Request):
    # Redirect to Google for authorization
    redirect_uri = request.url_for('auth_callback')
    
    # Force https on Vercel to avoid 'invalid_client' or redirect mapping issues
    if "vercel.app" in str(request.base_url) or os.getenv("VERCEL"):
        redirect_uri = str(redirect_uri).replace("http://", "https://")
        
    print(f"DEBUG: OAuth Redirect URI: {redirect_uri}")
    
    if not os.getenv('GOOGLE_CLIENT_ID'):
        print("ERROR: GOOGLE_CLIENT_ID not found in environment!")
        return RedirectResponse(url='/login?error=Configuration missing', status_code=status.HTTP_302_FOUND)
        
    return await oauth.google.authorize_redirect(request, redirect_uri)

@app.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        print(f"OAuth Error: {e}")
        return RedirectResponse(url='/login?error=OAuth failed', status_code=status.HTTP_302_FOUND)
    
    user_info = token.get('userinfo')
    if not user_info:
        return RedirectResponse(url='/login?error=No user info', status_code=status.HTTP_302_FOUND)
    
    email = user_info.get('email')
    full_name = user_info.get('name', 'Google User')
    
    # Check if user exists, otherwise create
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        # Create Google User with a random password since they use OAuth
        hashed_pw = get_password_hash(os.urandom(24).hex())
        user = models.User(email=email, hashed_password=hashed_pw, full_name=full_name, contact_number=None)
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
            {"value": "A", "text": "A quiet morning with a book/coffee.", "image": "/static/images/assessment/q1_a.png"},
            {"value": "B", "text": "A high-energy concert with a crowd.", "image": "/static/images/assessment/q1_b.png"}
        ]
    },
    {
        "id": "Q2_Communication",
        "title": "Communication",
        "options": [
            {"value": "A", "text": "Sending a carefully crafted email.", "image": "/static/images/assessment/q2_a.png"},
            {"value": "B", "text": "Hopping on a quick, 'face-to-face' video call.", "image": "/static/images/assessment/q2_b.png"}
        ]
    },
    {
        "id": "Q3_Workspace",
        "title": "Workspace",
        "options": [
            {"value": "A", "text": "A private pod with noise-canceling headphones.", "image": "/static/images/assessment/q3_a.png"},
            {"value": "B", "text": "A bustling co-working space with open desks.", "image": "/static/images/assessment/q3_b.png"}
        ]
    },
    {
        "id": "Q4_ProblemSolving",
        "title": "Problem Solving",
        "options": [
            {"value": "A", "text": "Digging through Google/Manuals solo.", "image": "/static/images/assessment/q4_a.png"},
            {"value": "B", "text": "Bouncing ideas off a group on a whiteboard.", "image": "/static/images/assessment/q4_b.png"}
        ]
    },
    {
        "id": "Q5_MeetingRole",
        "title": "Meeting Role",
        "options": [
            {"value": "A", "text": "The person taking detailed, silent notes.", "image": "/static/images/assessment/q5_a.png"},
            {"value": "B", "text": "The person leading the brainstorm out loud.", "image": "/static/images/assessment/q5_b.png"}
        ]
    },
 {
        "id": "Q6_LearningStyle",
        "title": "Learning Style",
        "options": [
            {"value": "A", "text": "Watching a deep-dive documentary alone.", "image": "/static/images/assessment/q6_a.png"},
            {"value": "B", "text": "Attending a live, interactive workshop.", "image": "/static/images/assessment/q6_b.png"}
        ]
    },
    {
        "id": "Q7_GoalPath",
        "title": "Goal: Path",
        "options": [
            {"value": "A", "text": "A straight highway with a clear destination.", "image": "/static/images/assessment/q7_a.png"},
            {"value": "B", "text": "A winding trail through a beautiful forest.", "image": "/static/images/assessment/q7_b.png"}
        ]
    },
    {
        "id": "Q8_GoalVision",
        "title": "Goal: Vision",
        "options": [
            {"value": "A", "text": "I have a 'Dream Job' title in my head.", "image": "/static/images/assessment/q8_a.png"},
            {"value": "B", "text": "I have a 'Lifestyle' I want, but the job is tbd.", "image": "/static/images/assessment/q8_b.png"}
        ]
    },
    {
        "id": "Q9_GoalSpeed",
        "title": "Goal: Speed",
        "options": [
            {"value": "A", "text": "I want to specialize and be the best at one thing.", "image": "/static/images/assessment/q9_a.png"},
            {"value": "B", "text": "I want to be a 'Jack of all trades' and know a bit of everything.", "image": "/static/images/assessment/q9_b.png"}
        ]
    },
    {
        "id": "Q10_GoalChoice",
        "title": "Goal: Choice",
        "options": [
            {"value": "A", "text": "I’d pick the 'Safe & Known' successful path.", "image": "/static/images/assessment/q10_a.png"},
            {"value": "B", "text": "I’d pick the 'Wildcard' path with high potential.", "image": "/static/images/assessment/q10_b.png"}
        ]
    }
]


# --- Assessment Routes ---

@app.get("/assessment/start")
async def assessment_start(request: Request, class_level: str, db: Session = Depends(get_db)):
    """Phase 1: Class Selection"""
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Check/Create Result
    result = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    if not result:
        result = models.AssessmentResult(user_id=user.id)
        db.add(result)
    
    # Save Phase 1 Selection
    result.selected_class = class_level
    db.commit()
    
    # Proceed to Phase 2 (Archetype)
    return RedirectResponse(url="/assessment", status_code=status.HTTP_302_FOUND)


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
        # Generate Analysis using Fallback Strategy
        try:
            clean_text = generate_content_with_fallback(prompt)
            result_data = json.loads(clean_text)
        except Exception as e:
            print(f"Analysis Error: {e}")
            result_data = {
                "phase_2_category": "Focused Specialist",
                "personality": "Ambivert",
                "goal_status": "Exploring",
                "confidence": 0.5,
                "reasoning": "AI Analysis unavailable. Default profile assigned based on answers."
            }

    # 4. Save to DB
    existing_result = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    
    if existing_result:
        # Update existing
        existing_result.phase_2_category = result_data.get("phase_2_category")
        existing_result.personality = result_data.get("personality")
        existing_result.goal_status = result_data.get("goal_status")
        existing_result.confidence = result_data.get("confidence")
        existing_result.reasoning = result_data.get("reasoning")
        existing_result.raw_answers = user_answers_data # This overwrites phase 1 raw answers if any, but selected_class is separate column
    else:
        # Create new
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

    # 2. Fetch all users
    all_users = db.query(models.User).all()

    # 3. Fetch all feedback
    all_feedback = db.query(models.Feedback).order_by(models.Feedback.timestamp.desc()).all()
    
    return templates.TemplateResponse("admin_dashboard.html", {
        "request": request, 
        "user": user, 
        "users": all_users,
        "feedbacks": all_feedback
    })

@app.post("/admin/users/{user_id}/delete")
async def delete_user(user_id: int, request: Request, db: Session = Depends(get_db)):
    # 1. Check admin auth
    current_user = get_current_user(request, db)
    if not current_user: # In a real app, check role="admin"
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # 2. Get User
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_delete:
         raise HTTPException(status_code=404, detail="User not found")

    # 3. Delete Assessment Result first (ForeignKey)
    if user_to_delete.assessment:
        db.delete(user_to_delete.assessment)
    
    # 4. Delete User
    db.delete(user_to_delete)
    db.commit()
    
    return RedirectResponse(url="/admin", status_code=status.HTTP_302_FOUND)


# --- Phase 3 Routes ---

from data.questions_phase3 import CATEGORY_SCENARIOS_MAP

@app.get("/assessment/phase3", response_class=HTMLResponse)
async def assessment_phase3(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Get user's Phase 2 result
    result = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    if not result or not result.phase_2_category:
        # No category to deep dive into
        return RedirectResponse(url="/assessment/result", status_code=status.HTTP_302_FOUND)

    category = result.phase_2_category
    scenarios = CATEGORY_SCENARIOS_MAP.get(category)
    
    if not scenarios:
        # Fallback if category not found or has no scenarios yet
        # For now, maybe just show Focused Specialist as default or error
        # Be safe and redirect w/ maybe a flash message (not impl yet)
        return RedirectResponse(url="/assessment/result", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("assessment_phase3.html", {
        "request": request, 
        "user": user, 
        "scenarios": scenarios,
        "category_name": category
    })

@app.post("/assessment/phase3/submit")
async def assessment_phase3_submit(
    request: Request, 
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    try:
        form_data = await request.form()
    except Exception:
        # Client disconnected or bad request
        return RedirectResponse(url="/assessment/phase3", status_code=status.HTTP_302_FOUND)
    answers = {}
    
    for key, value in form_data.items():
        answers[key] = value

    # Save to DB
    result = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    if not result:
        # Should likely have a phase 2 result first, but if not, create new?
        # For simplicity, we assume result exists. If not, redirect to start.
        return RedirectResponse(url="/assessment", status_code=status.HTTP_302_FOUND)
    
    result.phase3_answers = answers
    result.phase3_result = "Phase 3 Completed" # Placeholder
    
    # Generate Phase 3 Analysis using Gemini
    category = result.phase_2_category
    prompt_p3 = f"""
    Analyze these scenario responses for a student identified as '{category}' (Class 10 level).
    
    Scenarios & Answers:
    {json.dumps(answers, indent=2)}
    
    Provide a specific, actionable advice paragraph (approx 3-4 sentences) focusing on their work style preferences revealed by these choices. 
    Reflect on how they fit into the '{category}' archetype based on these nuances.
    """
    
    try:
         result.phase3_analysis = generate_content_with_fallback(prompt_p3)
    except Exception as e:
         result.phase3_analysis = f"Analysis unavailable at this time. ({str(e)})"
        
    db.commit()

    return RedirectResponse(url="/assessment/result", status_code=status.HTTP_302_FOUND)


# --- Phase 4 Routes (Final Stream Assessment) ---

from data.questions_final import all_questions, section_a_questions, section_b_questions, section_c_questions, section_d_questions
from data.questions_12th import questions_12th
from data.questions_above_12th import questions_above_12th

@app.get("/assessment/final", response_class=HTMLResponse)
async def assessment_final(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Get user class selection
    result = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    selected_class = result.selected_class if result else "10th" # Default to 10th if not found

    context = {
        "request": request, 
        "user": user,
    }

    if selected_class == "12th":
        context["mode"] = "12th"
        context["questions"] = questions_12th
    elif selected_class == "Above 12th": # Ensure this matches the exact string saved in Phase 1
        context["mode"] = "above"
        context["questions"] = questions_above_12th
    else:
        # Default to Class 10th (Existing Logic)
        context["mode"] = "10th"
        context["sections"] = all_questions

    return templates.TemplateResponse("assessment_final.html", context)

@app.post("/assessment/final/submit")
async def assessment_final_submit(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    form_data = await request.form()
    answers = {}
    mode = form_data.get("mode", "10th") # Default to 10th if missing
    print(f"DEBUG: Submitting Final Assessment. Mode: {mode}")

    for key, value in form_data.items():
        if key != "mode":
            answers[key] = value
        
    # fetch result object
    result = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    
    # --- Logic Branching based on Mode ---
    
    if mode == "10th":
        # ... EXISTING LOGIC FOR CLASS 10 (PCM/PCB/COMM/ARTS/VOC) ...
        # (Keeping the original rule-based scoring for Class 10 reliability)
        scores = { "PCM": 0, "PCB": 0, "COMM": 0, "ARTS": 0, "VOC": 0 }
        
        def add_points(streams, points=1):
            for s in streams:
                if s in scores: scores[s] += points

        # 1. Section A
        for q in section_a_questions:
            if answers.get(q["id"]) == q["correct_value"]:
                add_points(q["mapped_streams"], points=2)

        # 2. Preference Sections
        preference_questions = section_b_questions + section_c_questions + section_d_questions
        for q in preference_questions:
            user_ans = answers.get(q["id"])
            if not user_ans: continue
            selected_opt = next((opt for opt in q["options"] if opt["value"] == user_ans), None)
            if selected_opt and "stream" in selected_opt:
                 add_points([selected_opt["stream"]], points=1)
            else:
                if user_ans == "a":
                    txt = q["question"] + " " + (selected_opt["text"] if selected_opt else "")
                    if any(x in txt.lower() for x in ["plant", "health", "bio", "nutri", "species", "cures"]):
                         add_points(["PCB"], points=1)
                    else:
                         add_points(["PCM"], points=1)
                elif user_ans == "b": add_points(["COMM"], points=1)
                elif user_ans == "c": add_points(["ARTS"], points=1)
                elif user_ans == "d": add_points(["VOC"], points=1)

        # 3. Phase 2 Influence
        if result and result.phase_2_category:
            cat = result.phase_2_category
            if cat == "Focused Specialist": add_points(["PCM", "PCB"], points=3)
            elif cat == "Quiet Explorer": add_points(["PCB", "ARTS"], points=3)
            elif cat == "Visionary Leader": add_points(["COMM", "ARTS"], points=3)
            elif cat == "Strategic Builder": add_points(["PCM", "COMM"], points=3)
            elif cat == "Adaptive Explorer": add_points(["ARTS", "VOC"], points=3)
            elif cat == "Dynamic Generalist": add_points(["COMM", "VOC"], points=3)

        sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        winner_code = sorted_scores[0][0]
        code_map = { "PCM": "Science (PCM)", "PCB": "Science (PCB)", "COMM": "Commerce", "ARTS": "Arts & Humanities", "VOC": "Vocational Studies" }
        winner_name = code_map.get(winner_code, winner_code)
        
        # Save Score & Result
        if result:
            result.stream_scores = scores
            result.recommended_stream = winner_name

    else:
        # --- Logic for Class 12th & Above (No fixed scoring, pure AI Analysis) ---
        # We don't have a specific "stream" to recommend in the same way, but we will use the field for the primary recommendation
        scores = {} # Not used
        winner_name = "See Analysis" # Placeholder
        if result:
            result.stream_scores = {}
            result.recommended_stream = "AI Analyzing..." # Temporary

    # --- Common Save ---
    if result:
        result.final_answers = answers
        
        # --- AI Analysis (Gemini) ---
        if GEMINI_API_KEY:
            try:
                # Prepare Prompt based on Mode
                readable_answers = []
                
                if mode == "10th":
                     def get_question_text(q_id):
                        for section in all_questions.values():
                            for q in section["questions"]:
                                if q["id"] == q_id: return q["question"], q["options"]
                        return None, None
                     for q_id, ans_value in answers.items():
                        q_text, options = get_question_text(q_id)
                        if q_text:
                            selected_option = next((opt for opt in options if opt["value"] == ans_value), None)
                            ans_text = selected_option["text"] if selected_option else "Unknown"
                            readable_answers.append(f"Question: {q_text}\nSelected Answer: {ans_text}")
                
                elif mode == "12th":
                     # Use questions_12th data
                     q_map = {q["id"]: q for q in questions_12th}
                     for q_id, ans_text in answers.items():
                         if q_id in q_map:
                             readable_answers.append(f"Scenario: {q_map[q_id]['title']}\nInsight: {q_map[q_id]['insight']}\nUser Response: {ans_text}")

                elif mode == "above":
                     # Use questions_above_12th data
                     q_map = {q["id"]: q for q in questions_above_12th}
                     for q_id, ans_text in answers.items():
                         if q_id in q_map:
                             readable_answers.append(f"Question: {q_map[q_id]['title']}\nContext: {q_map[q_id]['insight']}\nUser Response: {ans_text}")

                answers_summary = "\n\n".join(readable_answers)
                phase2_cat = result.phase_2_category or "Unknown"
                
                # Dynamic Prompt Construction based on Class
                if mode == "10th":
                    task_instruction = f"""
                    1. The student's calculated best fit based on answers is "{winner_name}". Validate and Analyze this choice.
                    2. Provide a "Final Analysis" (approx 150 words) explaining WHY {winner_name} is the best fit based on their answers.
                    3. Provide 3 "Pros" (Why {winner_name} is good for the student).
                    4. Provide 3 "Cons" (Challenges to consider).
                    """
                    output_format = """
                    {
                      "recommended_stream": "Exact Stream Name",
                      "final_analysis": "Detailed explanation...",
                      "stream_pros": ["Pro 1", "Pro 2", "Pro 3"],
                      "stream_cons": ["Con 1", "Con 2", "Con 3"]
                    }
                    """
                elif mode == "12th":
                    task_instruction = """
                    1. Identify the Top 3 Career Goals / University Majors best suited for this student based on their scenarios.
                    2. For EACH goal, provide a specific "Reason" why they should go for that.
                    3. For EACH goal, provide 2 "Pros" (Advantages) and 2 "Cons" (Challenges).
                    4. Provide a "Final Analysis" (approx 100 words) summarizing their potential.
                    """
                    output_format = """
                    {
                      "recommended_stream": "Primary Field (e.g. Technology, Healthcare, Creative Arts)",
                      "final_analysis": "Summary...",
                      "goal_options": [
                        {
                            "title": "Option 1 Title", 
                            "reason": "Why they should choose this...",
                            "pros": ["Pro 1", "Pro 2"],
                            "cons": ["Con 1", "Con 2"]
                        },
                        {
                            "title": "Option 2 Title", 
                            "reason": "Why they should choose this...",
                            "pros": ["Pro 1", "Pro 2"],
                            "cons": ["Con 1", "Con 2"]
                        },
                        {
                            "title": "Option 3 Title", 
                            "reason": "Why they should choose this...",
                            "pros": ["Pro 1", "Pro 2"],
                            "cons": ["Con 1", "Con 2"]
                        }
                      ]
                    }
                    """
                else: # Above 12th
                    task_instruction = """
                    1. Identify the Top 3 Professional Roles / Niche Career Paths best suited for this student.
                    2. For EACH goal, provide a specific "Reason" why they should pursue it.
                    3. For EACH goal, provide 2 "Pros" (Advantages) and 2 "Cons" (Challenges).
                    4. Provide a "Final Analysis" (approx 100 words) on their professional outlook.
                    """
                    output_format = """
                    {
                      "recommended_stream": "Primary Field / Industry",
                      "final_analysis": "Summary...",
                      "goal_options": [
                        {
                            "title": "Role 1 Title", 
                            "reason": "Why this fits...",
                            "pros": ["Pro 1", "Pro 2"],
                            "cons": ["Con 1", "Con 2"]
                        },
                        {
                            "title": "Role 2 Title", 
                            "reason": "Why this fits...",
                            "pros": ["Pro 1", "Pro 2"],
                            "cons": ["Con 1", "Con 2"]
                        },
                        {
                            "title": "Role 3 Title", 
                            "reason": "Why this fits...",
                            "pros": ["Pro 1", "Pro 2"],
                            "cons": ["Con 1", "Con 2"]
                        }
                      ]
                    }
                    """

                prompt = f"""
                You are an expert career counselor. Analyze this profile for a {mode} grade student.

                Profile:
                - Archetype: {phase2_cat}
                - Answers:
                {answers_summary}

                Task:
                {task_instruction}

                Output MUST be raw JSON only matching this structure. Do not include markdown formatting or explanation text.
                {output_format}
                """
                
                # Generate Content with Fallback
                text = generate_content_with_fallback(prompt)
                print(f"DEBUG: AI Raw Text: {text}")
                ai_data = json.loads(text)
                
                if mode != "10th" and "recommended_stream" in ai_data: 
                     result.recommended_stream = ai_data["recommended_stream"]
                if "final_analysis" in ai_data: result.final_analysis = ai_data["final_analysis"]
                
                # Handling Data Mapping
                if mode == "10th":
                    if "stream_pros" in ai_data: result.stream_pros = ai_data["stream_pros"]
                    if "stream_cons" in ai_data: result.stream_cons = ai_data["stream_cons"]
                else:
                    # Map 'goal_options' to 'stream_pros' for storage
                    if "goal_options" in ai_data: result.stream_pros = ai_data["goal_options"]
                    result.stream_cons = [] # Not used for 12th/Above
                    
            except Exception as e:
                print(f"AI Analysis Failed: {e}")
                result.final_analysis = f"AI Analysis Unavailable. (Error: {str(e)})"
        else:
             result.final_analysis = "AI Analysis Unavailable (API Key missing)."

        db.commit()

    return RedirectResponse(url="/assessment/result", status_code=status.HTTP_302_FOUND)


# --- Chatbot Routes ---

class ChatRequest(BaseModel):
    message: str

@app.get("/chatbot", response_class=HTMLResponse)
async def chatbot_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    # Fetch History
    history = db.query(models.ChatMessage).filter(models.ChatMessage.user_id == user.id).order_by(models.ChatMessage.timestamp).all()
    
    return templates.TemplateResponse("chatbot.html", {"request": request, "user": user, "history": history})

# --- Chatbot Routes ---

@app.post("/chatbot/message")
async def chatbot_message(request: Request, chat_req: ChatRequest, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_message = chat_req.message
    
    # Save User Message
    user_msg_db = models.ChatMessage(user_id=user.id, sender="user", content=user_message)
    db.add(user_msg_db)
    db.commit()
    
    # 1. Build Context from DB
    result = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    
    context_str = f"User Name: {user.full_name}\n"
    if result:
        if result.selected_class:
            context_str += f"Class/Grade: {result.selected_class}\n"
        if result.phase_2_category:
            context_str += f"Personality Archetype: {result.phase_2_category}\n"
        if result.recommended_stream:
            context_str += f"Recommended Path: {result.recommended_stream}\n"
        
        # Add slight detail if available
        if result.phase3_analysis:
             context_str += f"Work Style Analysis: {result.phase3_analysis[:200]}...\n"

    # Fetch recent history for context
    recent_history = db.query(models.ChatMessage).filter(models.ChatMessage.user_id == user.id).order_by(models.ChatMessage.timestamp.desc()).limit(10).all()
    recent_history.reverse() # Oldest first
    history_str = "\n".join([f"{msg.sender.upper()}: {msg.content}" for msg in recent_history])

    # 2. Construct System Prompt
    prompt = f"""
    You are 'NextStep AI', an expert career counselor and student mentor.
    
    USER CONTEXT:
    {context_str}

    CONVERSATION HISTORY:
    {history_str}

    YOUR GOAL:
    Help the student with their career questions.
    - If they have assessment results, REFER TO THEM to make advice personalized.
    - If they don't, ask clarifying questions to help them.
    - Be encouraging, positive, and realistic.
    - Keep answers concise (under 200 words) unless asked for deep detail.
    - Use Markdown for bolding key terms or lists.
    - Reply to the latest STUDENT MESSAGE.

    STUDENT MESSAGE:
    {user_message}
    """
    
    # 3. Stream Gemini Response
    async def generate():
        full_response_text = ""
        try:
            if GEMINI_API_KEY:
                model = genai.GenerativeModel("gemini-flash-latest")
                response = model.generate_content(prompt, stream=True)
                for chunk in response:
                    if chunk.text:
                        text_chunk = chunk.text
                        full_response_text += text_chunk
                        yield text_chunk
            else:
                 # Demo Mode Simulation
                 fake_response = "I'm in demo mode (No API Key). Based on your profile, I'd suggest exploring based on your interests! (Please set GEMINI_API_KEY to get real AI responses)"
                 for word in fake_response.split():
                     text_chunk = word + " "
                     full_response_text += text_chunk
                     yield text_chunk
                     import time
                     time.sleep(0.05) # Fake delay
            
            # Save AI Message
            ai_msg_db = models.ChatMessage(user_id=user.id, sender="ai", content=full_response_text)
            db.add(ai_msg_db)
            db.commit()

        except Exception as e:
            print(f"Chat Error: {e}")
            error_msg = f"I'm having a little trouble thinking right now. (Error: {str(e)})"
            yield error_msg
            ai_msg_db = models.ChatMessage(user_id=user.id, sender="ai", content=error_msg)
            db.add(ai_msg_db)
            db.commit()

    return StreamingResponse(generate(), media_type="text/plain")


# --- Feedback Routes ---

@app.get("/feedback", response_class=HTMLResponse)
async def feedback_page(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("feedback.html", {"request": request, "user": user})

@app.post("/feedback")
async def submit_feedback(
    request: Request,
    content: str = Form(...),
    rating: int = Form(...),
    db: Session = Depends(get_db)
):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    new_feedback = models.Feedback(
        user_id=user.id,
        content=content,
        rating=rating
    )
    db.add(new_feedback)
    db.commit()
    
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)

