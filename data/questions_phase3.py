# ==========================================
# COUNSELLOR MODE: INTERACTIVE SCENARIOS
# ==========================================

# Category 1: Focused Specialist
# Theme: Depth, Precision, and Solitude
scenarios_focused_specialist = [
    {
        "id": "S1_TheBug",
        "title": "Fixing a Critical Bug",
        "story": "You are finishing an important team project. You spot a tiny logic error—one that might cause a failure in very rare cases. The project is already marked 'complete' by your lead. What is your immediate reaction?",
        "options": [
            {
                "value": "A",
                "text": "I fix it quietly in the background. It's cleaner that way, and we avoid a messy, distracting debate.",
                "outcome_hint": "Efficiency over protocol."
            },
            {
                "value": "B",
                "text": "I follow the protocol. I log the ticket and wait for the review. We have rules for a reason.",
                "outcome_hint": "Protocol over speed."
            }
        ]
    },
    {
        "id": "S2_TheWorkspace",
        "title": "Your Ideal Sanctuary",
        "story": "We all have an environment where we thrive. If you could snap your fingers and choose your workspace right now, which one feels right?",
        "options": [
            {
                "value": "A",
                "text": "The Cocoon. A small, windowless room with a lock. Total silence. Just me and the work.",
                "outcome_hint": "Deep isolation."
            },
            {
                "value": "B",
                "text": "The Sanctum. A high-tech lab. It has a 'quiet hour,' but the rest of the day I'm near my team.",
                "outcome_hint": "Balanced environment."
            }
        ]
    },
    {
        "id": "S3_TheMastery",
        "title": "Defining Your Legacy",
        "story": "I want you to picture your career ten years from now. A mentor offers you two distinct paths to mastery. Which one calls to you?",
        "options": [
            {
                "value": "A",
                "text": "To be 'The Needle.' The world's undisputed expert on one specific, deep niche.",
                "outcome_hint": "Niche depth."
            },
            {
                "value": "B",
                "text": "To be 'The Lantern.' A highly competent, respected engineer across the entire field.",
                "outcome_hint": "Broad competence."
            }
        ]
    },
    {
        "id": "S4_TheDeadline",
        "title": "The Pressure Cooker",
        "story": "Your deadline just got cut in half. The pressure is on. When the walls close in, what is your instinctual survival strategy?",
        "options": [
            {
                "value": "A",
                "text": "I go dark. Block the calendar, mute notifications, and focus. Distractions are the enemy.",
                "outcome_hint": "Individual focus."
            },
            {
                "value": "B",
                "text": "I divide and conquer. I grab a partner and we split the architecture to move faster together.",
                "outcome_hint": "Delegation/Collaboration."
            }
        ]
    },
    {
        "id": "S5_TheReward",
        "title": "The Recognition",
        "story": "You've just saved the company from a major issue. They want to thank you. Which form of gratitude actually means something to you?",
        "options": [
            {
                "value": "A",
                "text": "The Spotlight. A public award at the all-hands meeting. I want my name on the plaque.",
                "outcome_hint": "Public recognition."
            },
            {
                "value": "B",
                "text": "The Shadow. A quiet, significant bonus in my bank account and a private handshake.",
                "outcome_hint": "Private reward."
            }
        ]
    }
]

# Category 2: The Curious Researcher
# Theme: Discovery, Data, and Observation
scenarios_curious_researcher = [
    {
        "id": "S1_TheLibrary",
        "title": "The Distraction",
        "story": "You are organizing archives and a faded book falls out—totally unrelated to your work, but fascinating. Do you allow yourself to look?",
        "options": [
            {"value": "A", "text": "Yes. I read it. Following that curiosity is where the best ideas come from, even if it's 'inefficient'.", "outcome_hint": "Intellectual Curiosity"},
            {"value": "B", "text": "No. I put it back. I have a deadline and I need to stay disciplined.", "outcome_hint": "Focus/Discipline"}
        ]
    },
    {
        "id": "S2_ThePuzzle",
        "title": "The Unknown Data",
        "story": "A colleague hands you a mess of unlabeled data and asks if you can find anything interesting. How does that make you feel?",
        "options": [
            {"value": "A", "text": "Excited. It's a mystery waiting to be solved. I start categorizing immediately.", "outcome_hint": "Pattern seeking"},
            {"value": "B", "text": "Annoyed. It's a mess. I need proper documentation before I can work effectively.", "outcome_hint": "Rigorous standards"}
        ]
    },
    {
        "id": "S3_TheGroupProject",
        "title": "The Role Selection",
        "story": "We're assigning roles for a new project. Two spots are left. Which one feels like 'you'?",
        "options": [
            {"value": "A", "text": "The Archivist. I want to dig into the primary sources and find the truth.", "outcome_hint": "Deep Research"},
            {"value": "B", "text": "The Designer. I want to take that data and make it visually accessible to others.", "outcome_hint": "Information Design"}
        ]
    },
    {
        "id": "S4_TheObservation",
        "title": "The Crowded Room",
        "story": "You are at a mandatory social mixer. The room is loud. Where does your mind go?",
        "options": [
            {"value": "A", "text": "I start people-watching. I observe the social dynamics like a silent study.", "outcome_hint": "Observational analysis"},
            {"value": "B", "text": "I start planning my exit. I map the room to find the quickest way out.", "outcome_hint": "Strategic withdrawal"}
        ]
    },
    {
        "id": "S5_TheMystery",
        "title": "The Contract",
        "story": "You have a choice of assignment. Which timeline appeals to your way of thinking?",
        "options": [
            {"value": "A", "text": "The Cold Case. 12 months of solitary, slow, detailed analysis.", "outcome_hint": "Long-term depth"},
            {"value": "B", "text": "The Tech Glitch. 72 hours of high-pressure sprinting to find a root cause.", "outcome_hint": "High-pressure problem solving"}
        ]
    }
]

# Category 3: The Bold Driver
# Theme: Action, Risk, and Leadership
scenarios_bold_driver = [
    {
        "id": "S1_ThePitch",
        "title": "The Elevator Moment",
        "story": "The doors open and it's just you and the CEO. You have a bold, risky idea. Do you speak up now?",
        "options": [
            {"value": "A", "text": "Yes. I pitch it immediately. Fortune favors the bold.", "outcome_hint": "High risk/aggression"},
            {"value": "B", "text": "No. Unsolicited pitching is unprofessional. I'll book a proper meeting.", "outcome_hint": "Calculated/Professional"}
        ]
    },
    {
        "id": "S2_TheTeam",
        "title": "The Underperformer",
        "story": "Your star salesperson has missed their target twice in a row. You call them in. What is your approach?",
        "options": [
            {"value": "A", "text": "Tough Love. 'This is unacceptable. Fix it by Friday or we have to make changes.'", "outcome_hint": "Performance driven"},
            {"value": "B", "text": "Coaching. 'I know you can do this. Let's make a plan together to get you back on track.'", "outcome_hint": "Supportive/Coaching"}
        ]
    },
    {
        "id": "S3_TheCompetition",
        "title": "The Rivalry",
        "story": "A competitor just launched a product identical to yours, months ahead of us. What is your command to the team?",
        "options": [
            {"value": "A", "text": "'Work Harder.' We go to a war-room footing. We will out-execute them.", "outcome_hint": "Competitive/Sprint"},
            {"value": "B", "text": "'Pivot.' They won this round. Let's be smart and find a different angle.", "outcome_hint": "Strategic pivot"}
        ]
    },
    {
        "id": "S4_TheSpotlight",
        "title": "The Podium",
        "story": "You've won 'Leader of the Year.' You're at the microphone. What is your speech style?",
        "options": [
            {"value": "A", "text": "I take the 10 minutes. I share a bold vision and own the room.", "outcome_hint": "Charismatic/Visionary"},
            {"value": "B", "text": "I say a quick 'Thank You.' I share the credit and get off stage fast.", "outcome_hint": "Humble/Efficient"}
        ]
    },
    {
        "id": "S5_TheRisk",
        "title": "The Offer",
        "story": "Two job offers sit on your desk. Which one makes your heart beat faster?",
        "options": [
            {"value": "A", "text": "The Startup. Low pay, high equity. 50% chance of failure, but massive upside.", "outcome_hint": "High Risk/Reward"},
            {"value": "B", "text": "The Corporation. High pay, stability, and influence in a proven system.", "outcome_hint": "Stability/Impact"}
        ]
    }
]

# Category 4: The Social Catalyst
# Theme: Connection, Empathy, and Energy
scenarios_social_catalyst = [
    {
        "id": "S1_TheEvent",
        "title": "The Wedding Request",
        "story": "Your best friend asks you to plan their 200-person wedding because 'you just get people.' How does that request feel?",
        "options": [
            {"value": "A", "text": "Thrilling. I'm already buzzing with themes. The chaos is my canvas.", "outcome_hint": "Social Orchestrator"},
            {"value": "B", "text": "Overwhelming. The emotional weight of 200 people sounds exhausting.", "outcome_hint": "Intimate connector (not large scale)"}
        ]
    },
    {
        "id": "S2_TheVariety",
        "title": "The Lifestyle",
        "story": "If you could design your ideal work lifestyle, which path would you walk?",
        "options": [
            {"value": "A", "text": "The Chameleon. A new city every month, constantly meeting new faces.", "outcome_hint": "Novelty/Breadth"},
            {"value": "B", "text": "The Conductor. A daily show in one community, building deep roots.", "outcome_hint": "Depth/Ritual"}
        ]
    },
    {
        "id": "S3_TheInfluence",
        "title": "The Brand",
        "story": "People describe you to others. What do they say is your superpower?",
        "options": [
            {"value": "A", "text": "'The Face.' You are the charismatic spokesperson who inspires the crowd.", "outcome_hint": "Public Figure"},
            {"value": "B", "text": "'The Heart.' You are the matchmaker behind the scenes connecting everyone.", "outcome_hint": "Community Builder"}
        ]
    },
    {
        "id": "S4_TheNewcomer",
        "title": "The Loner",
        "story": "You're at a mixer and see someone standing alone, looking awkward. What is your instinct?",
        "options": [
            {"value": "A", "text": "I go to them. I introduce myself immediately to bring them into the fold.", "outcome_hint": "Proactive includer"},
            {"value": "B", "text": "I wait. I smile to let them know I'm safe, but I respect their boundaries.", "outcome_hint": "Passive availability"}
        ]
    },
    {
        "id": "S5_TheBrainstorm",
        "title": "The Name Game",
        "story": "We need to name a new project in 2 hours. How do you want to do this?",
        "options": [
            {"value": "A", "text": "Group Session. Let's talk it out loud. The energy of the group sparks my ideas.", "outcome_hint": "Collaborative thinker"},
            {"value": "B", "text": "Quiet Reflection. Let me think alone or with one partner first. Groups distract me.", "outcome_hint": "Independent/Dyad thinker"}
        ]
    }
]

# Category 5: The Adaptable Strategist
# Theme: Systems, Efficiency, and Flexibility
scenarios_adaptable_strategist = [
    {
        "id": "S1_TheMeeting",
        "title": "The Kickoff",
        "story": "You are leading a project kickoff. What is your natural facilitation style?",
        "options": [
            {"value": "A", "text": "The Architect. I set the vision and the social vibe, then I delegate the details.", "outcome_hint": "Delegating Architect"},
            {"value": "B", "text": "The Hub. I orchestrate from the middle. I like facilitating every part of the process.", "outcome_hint": "Hands-on Facilitator"}
        ]
    },
    {
        "id": "S2_TheBridge",
        "title": "The Translator",
        "story": "You often find yourself translating between the 'Technical' team and the 'Sales' team. How does that role feel?",
        "options": [
            {"value": "A", "text": "Essential. I enjoy being the human bridge that makes the system work.", "outcome_hint": "Integrator"},
            {"value": "B", "text": "Draining. It feels like refereeing. I'd rather just have clear objectives.", "outcome_hint": "Specialist preference"}
        ]
    },
    {
        "id": "S3_TheEnergy",
        "title": "The Aftermath",
        "story": "You just finished a 4-hour high-stakes negotiation. It went well, but it was intense. What do you need right now?",
        "options": [
            {"value": "A", "text": "Silence. I need a solo walk or a quiet room to recharge.", "outcome_hint": "Introverted recharge"},
            {"value": "B", "text": "Debrief. I need to grab a colleague and talk through everything that just happened.", "outcome_hint": "Extroverted processing"}
        ]
    },
    {
        "id": "S4_TheStrategy",
        "title": "The Plan",
        "story": "A major threat has appeared. We need a strategy in 72 hours. How do you start?",
        "options": [
            {"value": "A", "text": "I plan solo first. I need 24 hours alone to build the framework before I hear opinions.", "outcome_hint": "Internal processor"},
            {"value": "B", "text": "I plan socially. I call a war-room brainstorm immediately. I think better out loud.", "outcome_hint": "External processor"}
        ]
    },
    {
        "id": "S5_TheOffice",
        "title": "The Layout",
        "story": "The company is moving to an open plan with some focus pods. What's your honest reaction?",
        "options": [
            {"value": "A", "text": "It's perfect. I can adapt my environment to my mood throughout the day.", "outcome_hint": "Flexible/Adaptive"},
            {"value": "B", "text": "It's a compromise. It's too distracting for deep work and too isolating for real fun.", "outcome_hint": "Separation preference"}
        ]
    }
]

# Category 6: The Versatile Seeker
# Theme: Novelty, Breadth, and Creativity
scenarios_versatile_seeker = [
    {
        "id": "S1_TheHobby",
        "title": "The Interest Check",
        "story": "I'm curious about your life outside work. If I asked you to list your hobbies, what would that look like?",
        "options": [
            {"value": "A", "text": "A list of 5+ unrelated things. Archery, baking, coding... I love being a beginner.", "outcome_hint": "Polymath/Dabbler"},
            {"value": "B", "text": "One or two deep passions that I've refined for years.", "outcome_hint": "Deep or indefinable"}
        ]
    },
    {
        "id": "S2_TheStartup",
        "title": "The Swiss Army Knife",
        "story": "A chaotic startup needs someone to handle Operations, HR, and Marketing all at once. Does that excite you?",
        "options": [
            {"value": "A", "text": "Yes! It's the ultimate playground. I get to learn everything.", "outcome_hint": "Generalist thrive"},
            {"value": "B", "text": "No. That sounds like I'll be an overworked master of none.", "outcome_hint": "Specialist preference"}
        ]
    },
    {
        "id": "S3_TheCollaboration",
        "title": "The Creative Process",
        "story": "We are designing a board game together. What is your preferred way to work?",
        "options": [
            {"value": "A", "text": "In a pair. I love the dialogue and synergy of bouncing ideas.", "outcome_hint": "Collaborative creation"},
            {"value": "B", "text": "Alone first. I want to develop my idiosyncratic vision before I get feedback.", "outcome_hint": "Solo creation"}
        ]
    },
    {
        "id": "S4_ThePrototype",
        "title": "The Follow Through",
        "story": "You've hacked together a functional, but ugly, prototype of a new idea. What do you want to do next?",
        "options": [
            {"value": "A", "text": "Hand it off. The joy was in the 'aha' moment. The polish feels like a slog.", "outcome_hint": "Starter/Inventor"},
            {"value": "B", "text": "Stay involved. I want to guide the polish. The job isn't done until it's perfect.", "outcome_hint": "Finisher/Polisher"}
        ]
    },
    {
        "id": "S5_TheLearning",
        "title": "The New Skill",
        "story": "You need to master a complex new software tool. How do you approach it?",
        "options": [
            {"value": "A", "text": "Socially. I find a workshop or a friend. I learn by doing and chatting.", "outcome_hint": "Social/Active learner"},
            {"value": "B", "text": "Solitary. I read the manual and study the theory in silence.", "outcome_hint": "Solitary/Theory learner"}
        ]
    }
]

# Lookup map matching database 'phase_2_category' strings
CATEGORY_SCENARIOS_MAP = {
    "Focused Specialist": scenarios_focused_specialist,
    "Quiet Explorer": scenarios_curious_researcher,       # Maps to "The Curious Researcher"
    "Visionary Leader": scenarios_bold_driver,            # Maps to "The Bold Driver"
    "Adaptive Explorer": scenarios_social_catalyst,       # Maps to "The Social Catalyst"
    "Strategic Builder": scenarios_adaptable_strategist,  # Maps to "The Adaptable Strategist"
    "Dynamic Generalist": scenarios_versatile_seeker      # Maps to "The Versatile Seeker"
}