from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import bcrypt

import os
import json
import google.generativeai as genai
from .analysis import generate_career_recommendations, generate_goals_and_path
from dotenv import load_dotenv

# Load Env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

from . import models
from .database import SessionLocal, engine, get_db
from data.questions_data import questions

# Create Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="NextStep")

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
    
    # Fetch class-level specific recommendations
    recommendations = db.query(models.StreamRecommendationAnalysis).filter(
        models.StreamRecommendationAnalysis.user_id == user.id
    ).all()

    return templates.TemplateResponse("result.html", {
        "request": request, 
        "user": user, 
        "result": result,
        "recommendations": recommendations
    })

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

    form_data = await request.form()
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
    
    #     try:
    #          model = genai.GenerativeModel("gemini-flash-latest")
    #          response = model.generate_content(prompt_p3)
    #          result.phase3_analysis = response.text.strip()
    #     except:
    #          result.phase3_analysis = "Analysis unavailable at this time."
    # else:
    #     result.phase3_analysis = f"Demo Analysis for {category}: You show a strong preference for deep work and individual contribution."
    
    # Placeholder for simple analysis without API
    result.phase3_analysis = f"Analysis for {category}: Based on your scenario choices, you show a consistent pattern of behavior aligned with your archetype."
        
    db.commit()

    return RedirectResponse(url="/assessment/result", status_code=status.HTTP_302_FOUND)


# --- Phase 4 Routes (Final Stream Assessment) ---

from data.questions_final import all_questions, section_a_questions, section_b_questions, section_c_questions, section_d_questions

@app.get("/assessment/final", response_class=HTMLResponse)
async def assessment_final(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("assessment_final.html", {
        "request": request, 
        "user": user, 
        "sections": all_questions
    })

@app.post("/assessment/final/submit")
async def assessment_final_submit(request: Request, db: Session = Depends(get_db)):
    user = get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

    form_data = await request.form()
    answers = {}
    for key, value in form_data.items():
        answers[key] = value
        
    # --- Scoring Logic ---
    scores = {
        "PCM": 0,
        "PCB": 0,
        "COMM": 0,
        "ARTS": 0,
        "VOC": 0
    }
    
    def add_points(streams, points=1):
        for s in streams:
            if s in scores:
                scores[s] += points

    # 1. Section A (Correctness -> Mapped Streams)
    for q in section_a_questions:
        user_ans = answers.get(q["id"])
        if user_ans == q["correct_value"]:
            add_points(q["mapped_streams"], points=2)

    # 2. Section B, C, D (Preference Mapping)
    preference_questions = section_b_questions + section_c_questions + section_d_questions
    
    for q in preference_questions:
        user_ans = answers.get(q["id"])
        if not user_ans: continue
        
        # Check if option has explicit stream mapping
        selected_opt = next((opt for opt in q["options"] if opt["value"] == user_ans), None)
        
        if selected_opt and "stream" in selected_opt:
             add_points([selected_opt["stream"]], points=1)
        else:
            # Fallback based on value a/b/c/d for Section D
            if user_ans == "a":
                # Distinguish PCB vs PCM for Sec D based on keywords
                txt = q["question"] + " " + (selected_opt["text"] if selected_opt else "")
                if any(x in txt.lower() for x in ["plant", "health", "bio", "nutri", "species", "cures"]):
                     add_points(["PCB"], points=1)
                else:
                     add_points(["PCM"], points=1)
            elif user_ans == "b":
                add_points(["COMM"], points=1)
            elif user_ans == "c":
                add_points(["ARTS"], points=1)
            elif user_ans == "d":
                add_points(["VOC"], points=1)

    # 3. Phase 2 Influence (Combining Results)
    # Fetch existing result to get Phase 2 Category
    result = db.query(models.AssessmentResult).filter(models.AssessmentResult.user_id == user.id).first()
    if result and result.phase_2_category:
        cat = result.phase_2_category
        # Bonus Points Map
        # Focused Specialist -> Science/Deep Work
        # Quiet Explorer -> Research/Science/Arts
        # Visionary Leader -> Commerce/Leadership
        # Strategic Builder -> Engineering (PCM) or Commerce
        # Adaptive Explorer -> Arts/Humanities or Vocational
        # Dynamic Generalist -> Broad interest
        
        if cat == "Focused Specialist":
            add_points(["PCM", "PCB"], points=3)
        elif cat == "Quiet Explorer":
            add_points(["PCB", "ARTS"], points=3)
        elif cat == "Visionary Leader":
            add_points(["COMM", "ARTS"], points=3)
        elif cat == "Strategic Builder":
            add_points(["PCM", "COMM"], points=3)
        elif cat == "Adaptive Explorer":
            add_points(["ARTS", "VOC"], points=3)
        elif cat == "Dynamic Generalist":
            add_points(["COMM", "VOC"], points=3)

    # Determine Winner
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    winner_code = sorted_scores[0][0]
    
    code_map = {
        "PCM": "Science (PCM)",
        "PCB": "Science (PCB)",
        "COMM": "Commerce",
        "ARTS": "Arts & Humanities",
        "VOC": "Vocational Studies"
    }
    winner_name = code_map.get(winner_code, winner_code)
    
    
    # Save to DB (Preliminary)
    if result:
        result.final_answers = answers
        result.stream_scores = scores
        result.recommended_stream = winner_name # Default to manual score
        
        # --- AI Analysis ---
        if GEMINI_API_KEY:
            try:
                # Create Readable Answer Summary
                readable_answers = []
                
                # Helper to find text
                def get_question_text(q_id):
                    for section in all_questions.values():
                        for q in section["questions"]:
                            if q["id"] == q_id:
                                return q["question"], q["options"]
                    return None, None

                for q_id, ans_value in answers.items():
                    q_text, options = get_question_text(q_id)
                    if q_text:
                        selected_option = next((opt for opt in options if opt["value"] == ans_value), None)
                        ans_text = selected_option["text"] if selected_option else "Unknown"
                        readable_answers.append(f"Question: {q_text}\nSelected Answer: {ans_text}")
                
                answers_summary = "\n\n".join(readable_answers)

                phase2_cat = result.phase_2_category or "Unknown"
                phase3_analysis = result.phase3_analysis or "Not completed"
                
                prompt = f"""
                You are an expert career counselor for Class 10 students. Analyze the following student profile to recommend the best academic stream.

                Student Profile:
                - Identified Archetype (Phase 2): {phase2_cat}
                - Deep Dive Analysis (Phase 3): {phase3_analysis}

                Phase 4 Assessment Answers (Aptitude, Interests, Personality, Scenarios):
                {answers_summary}

                Preliminary Rule-Based Scores:
                {json.dumps(scores, indent=2)}

                Task:
                1. Recommend the SINGLE best academic stream from: "Science (PCM)", "Science (PCB)", "Commerce", "Arts & Humanities", "Vocational Studies".
                2. Provide a "Final Analysis" (approx 150 words) explaining WHY this is the best fit. **IMPORTANT: Do NOT refer to question codes like FA1, FB2. Refer to the specific topics or skills mentioned in the answers.**
                3. Provide a list of 3 "Pros" (Why this is good for the student).
                4. Provide a list of 3 "Cons" (Challenges to consider).

                Output must be valid JSON only:
                {{
                  "recommended_stream": "Exact Stream Name",
                  "final_analysis": "Detailed explanation...",
                  "stream_pros": ["Pro 1", "Pro 2", "Pro 3"],
                  "stream_cons": ["Con 1", "Con 2", "Con 3"]
                }}
                """
                
                model = genai.GenerativeModel("gemini-flash-latest")
                response = model.generate_content(prompt)
                
                # clean formatting if necessary (remove ```json ... ```)
                text = response.text.replace("```json", "").replace("```", "").strip()
                ai_data = json.loads(text)
                
                if "recommended_stream" in ai_data:
                    result.recommended_stream = ai_data["recommended_stream"]
                if "final_analysis" in ai_data:
                    result.final_analysis = ai_data["final_analysis"]
                if "stream_pros" in ai_data:
                    result.stream_pros = ai_data["stream_pros"]
                if "stream_cons" in ai_data:
                    result.stream_cons = ai_data["stream_cons"]
                    
            except Exception as e:
                print(f"AI Analysis Failed: {e}")
                result.final_analysis = f"AI Analysis Unavailable. Recommendation based on scoring rules. (Error: {str(e)})"
        else:
             result.final_analysis = "AI Analysis Unavailable (API Key missing). Recommendation based on scoring rules."

        db.commit()

    # --- Generate Class-Level Specific Recommendations ---
    if result and result.selected_class:
        class_level = result.selected_class
        
        # For 11th class: Generate Career Suggestions
        if class_level in ["11", "11th"]:
            career_rec = await generate_career_recommendations(
                phase2_category=result.phase_2_category or "Unknown",
                phase3_analysis=result.phase3_analysis or "",
                phase3_answers=result.phase3_answers or {},
                final_answers=result.final_answers or {},
                stream_scores=result.stream_scores or {},
                recommended_stream=result.recommended_stream or ""
            )
            
            if career_rec:
                # Check if recommendation already exists for this user
                existing_rec = db.query(models.StreamRecommendationAnalysis).filter(
                    models.StreamRecommendationAnalysis.user_id == user.id,
                    models.StreamRecommendationAnalysis.class_level == class_level,
                    models.StreamRecommendationAnalysis.recommendation_type == "career"
                ).first()
                
                if existing_rec:
                    existing_rec.career_suggestions = career_rec.get("career_suggestions")
                    existing_rec.career_reasoning = career_rec.get("career_reasoning")
                else:
                    new_rec = models.StreamRecommendationAnalysis(
                        user_id=user.id,
                        class_level=class_level,
                        recommendation_type="career",
                        career_suggestions=career_rec.get("career_suggestions"),
                        career_reasoning=career_rec.get("career_reasoning")
                    )
                    db.add(new_rec)
                db.commit()
        
        # For 12th or above: Generate Goals & Pathways
        elif class_level in ["12", "12th", "above_12", "Above 12"]:
            goals_rec = await generate_goals_and_path(
                phase2_category=result.phase_2_category or "Unknown",
                phase3_analysis=result.phase3_analysis or "",
                phase3_answers=result.phase3_answers or {},
                final_answers=result.final_answers or {},
                stream_scores=result.stream_scores or {},
                recommended_stream=result.recommended_stream or "",
                class_level=class_level
            )
            
            if goals_rec:
                # Check if recommendation already exists for this user
                existing_rec = db.query(models.StreamRecommendationAnalysis).filter(
                    models.StreamRecommendationAnalysis.user_id == user.id,
                    models.StreamRecommendationAnalysis.class_level == class_level,
                    models.StreamRecommendationAnalysis.recommendation_type == "goals"
                ).first()
                
                if existing_rec:
                    existing_rec.goal_suggestions = goals_rec.get("goal_suggestions")
                    existing_rec.goal_reasoning = goals_rec.get("goal_reasoning")
                else:
                    new_rec = models.StreamRecommendationAnalysis(
                        user_id=user.id,
                        class_level=class_level,
                        recommendation_type="goals",
                        goal_suggestions=goals_rec.get("goal_suggestions"),
                        goal_reasoning=goals_rec.get("goal_reasoning")
                    )
                    db.add(new_rec)
                db.commit()

    return RedirectResponse(url="/assessment/result", status_code=status.HTTP_302_FOUND)
