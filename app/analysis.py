import json
import google.generativeai as genai
from typing import Optional, Dict, Any


async def generate_career_recommendations(
    phase2_category: str,
    phase3_analysis: str,
    phase3_answers: Dict,
    final_answers: Dict,
    stream_scores: Dict,
    recommended_stream: str
) -> Optional[Dict[str, Any]]:
    """
    Generate 3 career suggestions with reasons for 11th class students.
    """
    try:
        # Create readable summary
        answers_summary = "\n".join([f"- {k}: {v}" for k, v in phase3_answers.items()])
        
        prompt = f"""
        You are an expert career counselor. Based on the student's assessment profile for 11th grade, 
        recommend 3 specific CAREER PATHS (not just streams, but actual careers) that would suit them well.

        Student Profile:
        - Identified Archetype: {phase2_category}
        - Deep Dive Analysis: {phase3_analysis}
        - Recommended Stream: {recommended_stream}
        - Stream Scores: {json.dumps(stream_scores, indent=2)}

        Phase 3 Scenario Choices:
        {answers_summary}

        Task:
        1. Recommend 3 specific CAREER PATHS related to {recommended_stream} that match their personality and interests.
        2. For each career, explain WHY it's a good fit based on their assessment results.
        3. Consider both traditional and emerging career options.

        Output must be valid JSON only:
        {{
          "careers": [
            {{
              "title": "Career Name",
              "reason": "Why this fits the student based on their profile (2-3 sentences)"
            }},
            {{
              "title": "Career Name",
              "reason": "Why this fits the student based on their profile (2-3 sentences)"
            }},
            {{
              "title": "Career Name",
              "reason": "Why this fits the student based on their profile (2-3 sentences)"
            }}
          ],
          "overall_reasoning": "1-2 sentence summary of why these careers align with this student's profile"
        }}
        """
        
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(prompt)
        
        # Clean formatting
        text = response.text.replace("```json", "").replace("```", "").strip()
        ai_data = json.loads(text)
        
        return {
            "career_suggestions": ai_data.get("careers", []),
            "career_reasoning": ai_data.get("overall_reasoning", "")
        }
        
    except Exception as e:
        print(f"Career Generation Failed: {e}")
        return None


async def generate_goals_and_path(
    phase2_category: str,
    phase3_analysis: str,
    phase3_answers: Dict,
    final_answers: Dict,
    stream_scores: Dict,
    recommended_stream: str,
    class_level: str
) -> Optional[Dict[str, Any]]:
    """
    Generate 3 goals/pathways for 12th class students or above.
    """
    try:
        # Create readable summary
        answers_summary = "\n".join([f"- {k}: {v}" for k, v in phase3_answers.items()])
        
        goal_type = "post-12th pathways" if class_level == "12" else "higher education & career pathways"
        
        prompt = f"""
        You are an expert academic and career advisor. Based on the student's assessment profile,
        recommend 3 distinct {goal_type} they can pursue.

        Student Profile:
        - Identified Archetype: {phase2_category}
        - Deep Dive Analysis: {phase3_analysis}
        - Recommended Stream: {recommended_stream}
        - Stream Scores: {json.dumps(stream_scores, indent=2)}
        - Class Level: {class_level}

        Phase 3 Scenario Choices:
        {answers_summary}

        Task:
        1. Recommend 3 distinct and feasible GOALS or PATHWAYS the student can pursue after 12th grade.
        2. Each goal should align with {recommended_stream} and their personality type ({phase2_category}).
        3. Include both traditional university paths and alternative/modern options (startup, research, etc.).
        4. For each goal, provide a clear description of what it entails and why it suits them.

        Output must be valid JSON only:
        {{
          "goals": [
            {{
              "goal": "Goal/Pathway Title",
              "description": "Detailed description of this pathway and why it suits them (2-3 sentences)"
            }},
            {{
              "goal": "Goal/Pathway Title",
              "description": "Detailed description of this pathway and why it suits them (2-3 sentences)"
            }},
            {{
              "goal": "Goal/Pathway Title",
              "description": "Detailed description of this pathway and why it suits them (2-3 sentences)"
            }}
          ],
          "overall_reasoning": "1-2 sentence overview of how these pathways leverage their strengths"
        }}
        """
        
        model = genai.GenerativeModel("gemini-flash-latest")
        response = model.generate_content(prompt)
        
        # Clean formatting
        text = response.text.replace("```json", "").replace("```", "").strip()
        ai_data = json.loads(text)
        
        return {
            "goal_suggestions": ai_data.get("goals", []),
            "goal_reasoning": ai_data.get("overall_reasoning", "")
        }
        
    except Exception as e:
        print(f"Goal Generation Failed: {e}")
        return None
