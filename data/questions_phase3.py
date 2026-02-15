
# Category 1: Focused Specialist
scenarios_focused_specialist = [
    {
        "id": "S1_TheBug",
        "title": "Scenario 1: The Bug",
        "story": "You're running a final diagnostic on a critical subsystem you built. Your eye catches it: a single line of logic that, under a rare but possible condition, will cause a cascade failure. No one else has seen it. The project lead has already declared the module 'code complete.'",
        "options": [
            {
                "value": "A",
                "text": "Fix it silently. You deploy the patch as a 'minor optimization' in the nightly build. It's cleaner, safer, and the project moves forward without a distracting debate.",
                "outcome_hint": "Efficiency over protocol."
            },
            {
                "value": "B",
                "text": "Flag it for the meeting. You log a formal issue and wait for the weekly review. Protocol must be followed.",
                "outcome_hint": "Protocol over speed."
            }
        ]
    },
    {
        "id": "S2_TheWorkspace",
        "title": "Scenario 2: The Workspace",
        "story": "HR is reorganizing. You have a choice between two workspaces.",
        "options": [
            {
                "value": "A",
                "text": "The Cocoon: A small, windowless corner office with a solid, lockable door. Absolute silence. Permanent.",
                "outcome_hint": "Deep isolation."
            },
            {
                "value": "B",
                "text": "The Sanctum: A state-of-the-art lab with the best equipment. It has a strict, enforced 'Quiet Hour' from 9-10 AM daily. The rest of the day, it's a collaborative space.",
                "outcome_hint": "Balanced environment."
            }
        ]
    },
    {
        "id": "S3_TheMastery",
        "title": "Scenario 3: The Mastery",
        "story": "A visionary offers you a choice for your career path.",
        "options": [
            {
                "value": "A",
                "text": "The Needle: You will become the undisputed, world-leading expert on the failure modes of 19th-century tungsten filaments. Your opinion will be the final word.",
                "outcome_hint": "Niche depth."
            },
            {
                "value": "B",
                "text": "The Lantern: You will become a highly competent, well-regarded engineer across the entire field of historical illumination technologies.",
                "outcome_hint": "Broad competence."
            }
        ]
    },
    {
        "id": "S4_TheDeadline",
        "title": "Scenario 4: The Deadline",
        "story": "Your 4-week deadline just became a 2-week deadline. The task is complex but can be modularized.",
        "options": [
            {
                "value": "A",
                "text": "Cut & Focus. You immediately block your calendar, set communication to 'Do Not Disturb,' and dive in. Meetings are a tax on context switching.",
                "outcome_hint": "Individual focus."
            },
            {
                "value": "B",
                "text": "Divide & Conquer. You ask your manager for one capable partner to split the architecture into two clear streams.",
                "outcome_hint": "Delegation/Collaboration."
            }
        ]
    },
    {
        "id": "S5_TheReward",
        "title": "Scenario 5: The Reward",
        "story": "For solving a critical problem, you can choose your recognition.",
        "options": [
            {
                "value": "A",
                "text": "The Spotlight: A 'Visionary Award' presented at the all-hands meeting, with your name etched on a plaque in the lobby.",
                "outcome_hint": "Public recognition."
            },
            {
                "value": "B",
                "text": "The Shadow: A significant, discreet bonus deposited directly into your account, with a private 'thank you' from the CEO.",
                "outcome_hint": "Private reward."
            }
        ]
    },
    {
        "id": "S6_TheTool",
        "title": "Scenario 6: The Tool",
        "story": "You need to automate a daily data analysis. There's a popular, well-supported software package that does 85% of what you need.",
        "options": [
            {
                "value": "A",
                "text": "Use the existing tool. You'll adapt your process slightly to fit its logic. Efficiency is key.",
                "outcome_hint": "Pragmatism."
            },
            {
                "value": "B",
                "text": "Build your own. You'll write a custom script over the next two days that fits your mental model and workflow perfectly.",
                "outcome_hint": "Perfectionism/Control."
            }
        ]
    },
    {
        "id": "S7_TheResearch",
        "title": "Scenario 7: The Research",
        "story": "You must master a new, complex API to complete your task. Your learning method:",
        "options": [
            {
                "value": "A",
                "text": "The 500-page manual. You download the definitive PDF, start on page one, and build a foundational mental model.",
                "outcome_hint": "Deep theory."
            },
            {
                "value": "B",
                "text": "The 10-minute video. You find a 'Quick Start' tutorial, get the basic example running, and learn the rest through trial, error, and targeted searches.",
                "outcome_hint": "Rapid application."
            }
        ]
    },
    {
        "id": "S8_TheCommunication",
        "title": "Scenario 8: The Communication",
        "story": "You've conceived a more efficient architecture for a team project. How do you introduce it?",
        "options": [
            {
                "value": "A",
                "text": "Write a detailed memo. You draft a document with rationale, diagrams, trade-off analyses, and a migration plan. Distribute 24 hours before discussion.",
                "outcome_hint": "Structured communication."
            },
            {
                "value": "B",
                "text": "Sketch it on the whiteboard. You grab the team after a stand-up, draw the core concept, and talk it through in real-time.",
                "outcome_hint": "Dynamic communication."
            }
        ]
    },
    {
        "id": "S9_TheCriticism",
        "title": "Scenario 9: The Criticism",
        "story": "You've submitted a major design document for review. You ask for feedback in this format:",
        "options": [
            {
                "value": "A",
                "text": "A red-penciled document. Mark up the PDF with comments and tracked changes. Let me absorb your thoughts in my own time and space.",
                "outcome_hint": "Asynchronous/Reflective."
            },
            {
                "value": "B",
                "text": "A face-to-face sit-down. Let's walk through this together, in real time.",
                "outcome_hint": "Synchronous/Interactive."
            }
        ]
    },
    {
        "id": "S10_TheLongGame",
        "title": "Scenario 10: The Long Game",
        "story": "An oracle shows you your future: you will spend the next decade in relative solitude, studying, practicing, and refining a single, profound skill. Your gut reaction:",
        "options": [
            {
                "value": "A",
                "text": "'A Challenge.' This is the pure path. The depth of focus is the point.",
                "outcome_hint": "Solitary mastery."
            },
            {
                "value": "B",
                "text": "'A Sentence.' A decade of isolation is a cost too high, even for greatness. Mastery should be shared.",
                "outcome_hint": "Shared mastery."
            }
        ]
    }
]

# Category 2: The Curious Researcher
scenarios_curious_researcher = [
    {
        "id": "S1_TheLibrary",
        "title": "Scenario 1: The Library",
        "story": "You’re shelving books when a 60-year-faded volume slips out: 'The Nocturnal Migration Patterns of Arctic Moths, 1893.' Unrelated to your studies.",
        "options": [
            {"value": "A", "text": "Read it 'just because.' You fall down a rabbit hole of bizarre, beautiful facts. Inefficient but enriching.", "outcome_hint": "Intellectual Curiosity"},
            {"value": "B", "text": "Put it back. You reshelve it neatly. Your own research has a deadline.", "outcome_hint": "Focus/Discipline"}
        ]
    },
    {
        "id": "S2_ThePuzzle",
        "title": "Scenario 2: The Puzzle",
        "story": "A colleague drops a USB drive with 10,000 lines of unlabeled data. 'Just see if anything looks interesting?'",
        "options": [
            {"value": "A", "text": "Excited to find the pattern. This is a delicious mystery. You start categorizing and hypothesizing immediately.", "outcome_hint": "Pattern seeking"},
            {"value": "B", "text": "Annoyed by the mess. This is a data hygiene nightmare. You ask for documentation before touching it.", "outcome_hint": "Rigorous standards"}
        ]
    },
    {
        "id": "S3_TheGroupProject",
        "title": "Scenario 3: The Group Project",
        "story": "Roles are being assigned. Two are left: The Archivist (deep digging) and The Designer (formatting/visuals).",
        "options": [
            {"value": "A", "text": "The Archivist. You want to uncover the Truth in the primary sources. Your findings shape the narrative.", "outcome_hint": "Deep Research"},
            {"value": "B", "text": "The Designer. Making complex data visually accessible is its own form of discovery.", "outcome_hint": "Information Design"}
        ]
    },
    {
        "id": "S4_TheObservation",
        "title": "Scenario 4: The Observation",
        "story": "You’re at a mandatory mixer. The din is loud. No immediate escape.",
        "options": [
            {"value": "A", "text": "Watching the crowd. You observe social dynamics and compile a silent sociological study.", "outcome_hint": "Observational analysis"},
            {"value": "B", "text": "Finding the exit. You map the room and plan a route to leave gracefully and fast.", "outcome_hint": "Strategic withdrawal"}
        ]
    },
    {
        "id": "S5_TheMystery",
        "title": "Scenario 5: The Mystery",
        "story": "Two research contracts:",
        "options": [
            {"value": "A", "text": "The Cold Case. 6-12 months of solitary, detailed analysis of fragmented historical evidence.", "outcome_hint": "Long-term depth"},
            {"value": "B", "text": "The Tech Glitch. 72 hours to diagnose a catastrophic root cause from logs. High stakes sprint.", "outcome_hint": "High-pressure problem solving"}
        ]
    },
    {
        "id": "S6_TheOutput",
        "title": "Scenario 6: The Output",
        "story": "Your long-term project is concluding. How do you define its ultimate value?",
        "options": [
            {"value": "A", "text": "As a 'Discovery.' A new piece of knowledge/dataset that becomes a tool for others (citations).", "outcome_hint": "Academic impact"},
            {"value": "B", "text": "As a 'Service.' A direct, useful experience or guide that people actively use.", "outcome_hint": "Practical utility"}
        ]
    },
    {
        "id": "S7_TheNature",
        "title": "Scenario 7: The Nature",
        "story": "You can choose your environment for a week of analysis:",
        "options": [
            {"value": "A", "text": "The Glasshouse. Quiet, organic, sunlight. Stimulates lateral connection-making.", "outcome_hint": "Organic/Lateral thinking"},
            {"value": "B", "text": "The Digital Archive. Silent, no windows, vast data terminals. Pure information integration.", "outcome_hint": "Digital/Linear efficiency"}
        ]
    },
    {
        "id": "S8_TheRisk",
        "title": "Scenario 8: The Risk",
        "story": "A fellowship where the final 3 months are 'unscripted' and location-independent based on findings.",
        "options": [
            {"value": "A", "text": "Exciting. The unknown is the point. Using evidence to lead you into uncharted territory.", "outcome_hint": "Exploratory risk-taking"},
            {"value": "B", "text": "Stressful. Lack of structure is paralyzing. You prefer a defined hypothesis.", "outcome_hint": "Structured certainty"}
        ]
    },
    {
        "id": "S9_TheMedium",
        "title": "Scenario 9: The Medium",
        "story": "Explain a complex ecological process to non-specialist donors.",
        "options": [
            {"value": "A", "text": "A Written Report. Elegant prose for nuance and narrative arc.", "outcome_hint": "Verbal/Written communication"},
            {"value": "B", "text": "An Interactive Simulation. A web app variables to yield real-time effects.", "outcome_hint": "Systems thinking/Simulation"},
             {"value": "C", "text": "A Physical 3D Model. Tactile, layered landscape showing flows.", "outcome_hint": "Spatial/Tactile"}
        ]
    },
    {
        "id": "S10_TheChoice",
        "title": "Scenario 10: The Choice",
        "story": "A foundation offers a year to explore. You counter-propose:",
        "options": [
            {"value": "A", "text": "The 'Sampler'. Try 3 fields for 1 month each, then choose one for the remaining 9.", "outcome_hint": "Breadth first"},
            {"value": "B", "text": "Stick to original. Commit to full year of deep immersion in one field.", "outcome_hint": "Depth first"}
        ]
    }
]

# Category 3: The Bold Driver
scenarios_bold_driver = [
    {
        "id": "S1_ThePitch",
        "title": "Scenario 1: The Pitch",
        "story": "You see the CEO alone at the elevator. You have a bold, half-baked idea that could save millions.",
        "options": [
            {"value": "A", "text": "Pitch immediately. Unsolicited but high reward. You hand her a card with bullet points.", "outcome_hint": "High risk/aggression"},
            {"value": "B", "text": "Wait for appointment. Unsolicited is unprofessional. You book a slot to present a polished deck.", "outcome_hint": "Calculated/Professional"}
        ]
    },
    {
        "id": "S2_TheTeam",
        "title": "Scenario 2: The Team",
        "story": "Star salesperson Maya has missed targets twice. You call her in for:",
        "options": [
            {"value": "A", "text": "The 'Tough Love' Talk. 'This is unacceptable. Fix it by Friday or we reassign.'", "outcome_hint": "Performance driven"},
            {"value": "B", "text": "The 'Second Chance' Talk. 'I know you can do this. How can I help? Let's make a plan.'", "outcome_hint": "Supportive/Coaching"}
        ]
    },
    {
        "id": "S3_TheCompetition",
        "title": "Scenario 3: The Competition",
        "story": "Rival leaked a identical product 6 months ahead of you. Immediate reaction:",
        "options": [
            {"value": "A", "text": "Work Harder. War-room footing. 'Let's show them how it's DONE.' Aggressive deadlines.", "outcome_hint": "Competitive/Sprint"},
            {"value": "B", "text": "Feel Discouraged -> Pivot. Regroup, accept they won this race, and find a better niche/angle.", "outcome_hint": "Strategic pivot"}
        ]
    },
    {
        "id": "S4_TheSpotlight",
        "title": "Scenario 4: The Spotlight",
        "story": "You won 'Industry Leader of the Year.' At the podium:",
        "options": [
            {"value": "A", "text": "Give the 10-minute speech. Bold vision, personal story. You own the room.", "outcome_hint": "Charismatic/Visionary"},
            {"value": "B", "text": "Quick 'Thank You.' Share credit, be classy and fast.", "outcome_hint": "Humble/Efficient"}
        ]
    },
    {
        "id": "S5_TheRisk",
        "title": "Scenario 5: The Risk",
        "story": "Two job offers:",
        "options": [
            {"value": "A", "text": "The Startup. Low pay, high equity. 50% chance of failure but massive upside.", "outcome_hint": "High Risk/Reward"},
            {"value": "B", "text": "The Corporate. High pay, stability, influence in a proven system.", "outcome_hint": "Stability/Impact"}
        ]
    },
    {
        "id": "S6_TheStructure",
        "title": "Scenario 6: The Structure",
        "story": "Recruited for leadership:",
        "options": [
            {"value": "A", "text": "The Boss (Small). GM of a 50-person autonomous unit. You run it all.", "outcome_hint": "Autonomy/Control"},
            {"value": "B", "text": "The High-Ranking Officer (Large). SVP in 50k person org. Huge budget, complex politics.", "outcome_hint": "Scale/Influence"}
        ]
    },
    {
        "id": "S7_TheCrisis",
        "title": "Scenario 7: The Crisis",
        "story": "Flood at team offsite. Panic.",
        "options": [
            {"value": "A", "text": "Take the megaphone. Direct the response from high ground. Create order.", "outcome_hint": "Command & Control"},
            {"value": "B", "text": "Jump in the water. Physically save people. Lead by example in the thick of it.", "outcome_hint": "Servant/Action Leadership"}
        ]
    },
    {
        "id": "S8_TheSchedule",
        "title": "Scenario 8: The Schedule",
        "story": "Tomorrow is solid back-to-back meetings from 8:30 to 5:00.",
        "options": [
            {"value": "A", "text": "'Productive.' This is where decisions happen. You thrive on the momentum.", "outcome_hint": "High-velocity execution"},
            {"value": "B", "text": "'Exhausting.' This is a treadmill. You cancel two to create a focus block.", "outcome_hint": "Deep work priority"}
        ]
    },
    {
        "id": "S9_TheVision",
        "title": "Scenario 9: The Vision",
        "story": "Quarterly planning debate: Big Picture vs Daily Wins.",
        "options": [
            {"value": "A", "text": "Big Picture (5 Years). 'Forget easy wins. Build the foundation for the moonshot.'", "outcome_hint": "Long-term visionary"},
            {"value": "B", "text": "Daily Wins (Today). 'Momentum is everything. Stack visible victories now.'", "outcome_hint": "Short-term pragmatic"}
        ]
    },
    {
        "id": "S10_TheSocial",
        "title": "Scenario 10: The Social",
        "story": "Stalled negotiation with a hard-to-read CEO.",
        "options": [
            {"value": "A", "text": "A Dinner Party. Invite them and non-business guests to your home. Build genuine rapport.", "outcome_hint": "Relationship based"},
            {"value": "B", "text": "Final Boardroom Session. High-pressure, unbeatable term sheet. Logic and force.", "outcome_hint": "Transactional/Power"}
        ]
    }
]

# Category 4: The Social Catalyst
scenarios_social_catalyst = [
    {
        "id": "S1_TheEvent",
        "title": "Scenario 1: The Event",
        "story": "Best friend asks you to plan their 200-person wedding reception. 'You just GET people!'",
        "options": [
            {"value": "A", "text": "'In your element!' You buzz with themes and connection maps. The chaos is a creative canvas.", "outcome_hint": "Social Orchestrator"},
            {"value": "B", "text": "'Overwhelmed.' The logistical weight of that many people is crushing.", "outcome_hint": "Intimate connector (not large scale)"}
        ]
    },
    {
        "id": "S2_TheVariety",
        "title": "Scenario 2: The Variety",
        "story": "Two job offers:",
        "options": [
            {"value": "A", "text": "The Chameleon. Community lead for nomadic co-working. New city every month.", "outcome_hint": "Novelty/Breadth"},
            {"value": "B", "text": "The Conductor. Host of a local daily morning show. Deep, daily connection with familiar audience.", "outcome_hint": "Depth/Ritual"}
        ]
    },
    {
        "id": "S3_TheInfluence",
        "title": "Scenario 3: The Influence",
        "story": "Media profile brand question: 'What is your core brand?'",
        "options": [
            {"value": "A", "text": "'The Face.' Charismatic spokesperson. Broad, inspirational influence.", "outcome_hint": "Public Figure"},
            {"value": "B", "text": "'The Heart.' Behind-the-scenes matchmaker. Intimate, powerful network.", "outcome_hint": "Community Builder"}
        ]
    },
    {
        "id": "S4_TheNewcomer",
        "title": "Scenario 4: The Newcomer",
        "story": "Networking mixer. Someone is standing alone avoiding eye contact.",
        "options": [
            {"value": "A", "text": "Introduce yourself immediately. Bring him into the fold.", "outcome_hint": "Proactive includer"},
            {"value": "B", "text": "Wait for them. Respect boundaries; offer a smile but let them approach.", "outcome_hint": "Passive availability"}
        ]
    },
    {
        "id": "S5_TheBrainstorm",
        "title": "Scenario 5: The Brainstorm",
        "story": "Naming a new project in 2 hours. Your process:",
        "options": [
            {"value": "A", "text": "Talking out loud with a group. Energy bounces, ideas get wilder.", "outcome_hint": "Collaborative thinker"},
            {"value": "B", "text": "Talking to yourself/one other. Avoid groupthink to find a unique cohesive idea.", "outcome_hint": "Independent/Dyad thinker"}
        ]
    },
    {
        "id": "S6_TheTravel",
        "title": "Scenario 6: The Travel",
        "story": "Role as 'Cultural Storyteller': 3 weeks in new country every month living with locals.",
        "options": [
            {"value": "A", "text": "The Dream. Constant flow of new faces and stories is fuel.", "outcome_hint": "Global/Nomadic"},
            {"value": "B", "text": "A Nightmare. Rootless. You need a home base to recharge.", "outcome_hint": "Local/Rooted"}
        ]
    },
    {
        "id": "S7_TheFeedback",
        "title": "Scenario 7: The Feedback",
        "story": "Personal essay gets 500 glowing comments and 5 vicious trolls. What dominates your mind?",
        "options": [
            {"value": "A", "text": "The 500 Likes. Validation is energizing. Trolls are noise.", "outcome_hint": "Validation driven"},
            {"value": "B", "text": "The 5 Trolls. They sting. You wonder if they are right.", "outcome_hint": "Sensitivity/Criticism focused"}
        ]
    },
    {
        "id": "S8_TheConflict",
        "title": "Scenario 8: The Conflict",
        "story": "Two friends have a falling out. It poisons the group events.",
        "options": [
            {"value": "A", "text": "Bring them together. You mediate a sit-down. Risk yourself to restore the ecosystem.", "outcome_hint": "Active Mediator"},
            {"value": "B", "text": "Stay out of it. Listen individually but don't take sides.", "outcome_hint": "Peacekeeper/Neutral"}
        ]
    },
    {
        "id": "S9_ThePresentation",
        "title": "Scenario 9: The Presentation",
        "story": "Leading a session on 'The Art of Conversation'.",
        "options": [
            {"value": "A", "text": "Perform on Main Stage. Keynote to 1000. Inspirational storytelling.", "outcome_hint": "Performance/Broadcast"},
            {"value": "B", "text": "Small Interactive Class. Workshop with 30. Practice and personal feedback.", "outcome_hint": "Teaching/Facilitation"}
        ]
    },
    {
        "id": "S10_ThePivot",
        "title": "Scenario 10: The Pivot",
        "story": "New social app explodes.",
        "options": [
            {"value": "A", "text": "First to Join. Figure out rules, shape norms, invite friends.", "outcome_hint": "Early Adopter"},
            {"value": "B", "text": "The One Who Waits. Watch to see if it has staying power.", "outcome_hint": "Skeptic/Observer"}
        ]
    }
]

# Category 5: The Adaptable Strategist
scenarios_adaptable_strategist = [
    {
        "id": "S1_TheMeeting",
        "title": "Scenario 1: The Meeting",
        "story": "Leading a kickoff: Icebreaker -> Vision -> Breakout -> Synthesis.",
        "options": [
            {"value": "A", "text": "Lead social/vision, then delegate synthesis. Optimize for your energy spikes.", "outcome_hint": "Delegating Architect"},
            {"value": "B", "text": "Orchestrate from the middle. Facilitate everything. You are the steady central hub.", "outcome_hint": "Hands-on Facilitator"}
        ]
    },
    {
        "id": "S2_TheBridge",
        "title": "Scenario 2: The Bridge",
        "story": "You are the 'Translator' between engineering (specs) and sales (buzzwords).",
        "options": [
            {"value": "A", "text": "Natural and essential. You enjoy being the human API. The project runs smoother.", "outcome_hint": "Integrator"},
            {"value": "B", "text": "Exhausting and political. It feels like refereeing. You crave clear objectives.", "outcome_hint": " Specialist preference"}
        ]
    },
    {
        "id": "S3_TheEnergy",
        "title": "Scenario 3: The Energy",
        "story": "4-hour high stakes negotiation using all your skills.",
        "options": [
            {"value": "A", "text": "A 2-hour 'silent break' after. You need to recharge solo to be effective.", "outcome_hint": "Introverted recharge"},
            {"value": "B", "text": "Immediately debrief with a colleague. Processing out loud recharges you.", "outcome_hint": "Extroverted processing"}
        ]
    },
    {
        "id": "S4_TheStrategy",
        "title": "Scenario 4: The Strategy",
        "story": "Major threat. Counter-strategy needed in 72 hours.",
        "options": [
            {"value": "A", "text": "Plan Solo, Execute Socially. First 24h alone for framework, then team for buy-in.", "outcome_hint": "Internal processor"},
            {"value": "B", "text": "Plan Socially, Refine Solo. Immediate war room brainstorm, then refine alone.", "outcome_hint": "External processor"}
        ]
    },
    {
        "id": "S5_TheOffice",
        "title": "Scenario 5: The Office",
        "story": "New open plan with ring of 'focus pods'.",
        "options": [
            {"value": "A", "text": "The perfect hybrid. Autonomy within community. Adapt environment to mood.", "outcome_hint": "Flexible/Adaptive"},
            {"value": "B", "text": "Frustrating compromise. Too distracting for deep work, too isolating for chat.", "outcome_hint": "Separation preference"}
        ]
    },
    {
        "id": "S6_TheNegotiation",
        "title": "Scenario 6: The Negotiation",
        "story": "Tense vendor negotation. Aggressive rep.",
        "options": [
            {"value": "A", "text": "Listen more than speak. Let them exhaust themselves. Use silence.", "outcome_hint": "Passive/Analytical power"},
            {"value": "B", "text": "Match energy, then redirect. Interrupt firmly but politely. Control the flow.", "outcome_hint": "Active/Assertive power"}
        ]
    },
    {
        "id": "S7_TheManagement",
        "title": "Scenario 7: The Management",
        "story": "Promotion choice:",
        "options": [
            {"value": "A", "text": "Project Manager. Manage a system (tasks, resources) to a goal.", "outcome_hint": "System focused"},
            {"value": "B", "text": "Team Manager. Manage the human engine (careers, morale).", "outcome_hint": "People focused"}
        ]
    },
    {
        "id": "S8_TheEfficiency",
        "title": "Scenario 8: The Efficiency",
        "story": "Report due. 4 hours solo vs collaborative delegation (slower total).",
        "options": [
            {"value": "A", "text": "Do it alone. Speed and cohesion. Hero model.", "outcome_hint": "Efficiency/Control"},
            {"value": "B", "text": "Do it as a team. Development and buy-in, even if slower.", "outcome_hint": "Development/Slower"}
        ]
    },
    {
        "id": "S9_TheMood",
        "title": "Scenario 9: The Mood",
        "story": "4:55 PM, deep focus mode. Spontaneous team drinks?",
        "options": [
            {"value": "A", "text": "Flip the switch. Consciously shift gears and go be present.", "outcome_hint": "High adaptability"},
            {"value": "B", "text": "Politely decline. Brain still in model. Need a buffer.", "outcome_hint": "Low switch cost"}
        ]
    },
    {
        "id": "S10_TheGrowth",
        "title": "Scenario 10: The Growth",
        "story": "10-year career plan metaphor.",
        "options": [
            {"value": "A", "text": "Ladder (Up). Increasing authority in a coherent field.", "outcome_hint": "Vertical/Specialist"},
            {"value": "B", "text": "Web (Expanding). Portfolio of diverse skills and roles.", "outcome_hint": "Lateral/Generalist"}
        ]
    }
]

# Category 6: The Versatile Seeker
scenarios_versatile_seeker = [
    {
        "id": "S1_TheHobby",
        "title": "Scenario 1: The Hobby",
        "story": "Interest survey asks for top 3 hobbies.",
        "options": [
            {"value": "A", "text": "You have 5+ unrelated hobbies. Life is a tapestry of beginnings.", "outcome_hint": "Polymath/Dabbler"},
            {"value": "B", "text": "You have 1-2 deep ones, or none. You reject the label.", "outcome_hint": "Deep or indefinable"}
        ]
    },
    {
        "id": "S2_TheStartup",
        "title": "Scenario 2: The Startup",
        "story": "Startup needs a 'Swiss Army Knife' (Operations & Magic).",
        "options": [
            {"value": "A", "text": "Excited. Ultimate playground. Learn everything.", "outcome_hint": "Generalist thrive"},
            {"value": "B", "text": "Scared. Chronically overworked master of none.", "outcome_hint": "Specialist preference"}
        ]
    },
    {
        "id": "S3_TheCollaboration",
        "title": "Scenario 3: The Collaboration",
        "story": "Designing a board game. Work style:",
        "options": [
            {"value": "A", "text": "Work in a pair. Dialogue and synergy.", "outcome_hint": "Collaborative creation"},
            {"value": "B", "text": "Work alone, then feedback. Idiosyncratic vision first.", "outcome_hint": "Solo creation"}
        ]
    },
    {
        "id": "S4_ThePrototype",
        "title": "Scenario 4: The Prototype",
        "story": "You hacked a ugly functional prototype. Next:",
        "options": [
            {"value": "A", "text": "Hand it off. Joy was the 'aha'. Refinement is a slog.", "outcome_hint": "Starter/Inventor"},
            {"value": "B", "text": "Stay involved. Guide the polish. Follow-through is discovery.", "outcome_hint": "Finisher/Polisher"}
        ]
    },
    {
        "id": "S5_TheLearning",
        "title": "Scenario 5: The Learning",
        "story": "Mastering new 3D software.",
        "options": [
            {"value": "A", "text": "'Learning by Doing' with others. Workshop, chatter, trial.", "outcome_hint": "Social/Active learner"},
            {"value": "B", "text": "'Learning by Reading' alone. Manuals, deep theory, silence.", "outcome_hint": "Solitary/Theory learner"}
        ]
    },
    {
        "id": "S6_TheBalance",
        "title": "Scenario 6: The Balance",
        "story": "Return from 3-day solitary camping.",
        "options": [
            {"value": "A", "text": "Crave a party. Need to download and see faces.", "outcome_hint": "Cyclical recharge"},
            {"value": "B", "text": "Cherish quiet. Slow re-acclimation.", "outcome_hint": "Sustained solitude"}
        ]
    },
    {
        "id": "S7_TheMedium",
        "title": "Scenario 7: The Medium",
        "story": "Postgrad programs: Science Illustration vs Sonic Info Design.",
        "options": [
            {"value": "A", "text": "'Perfect—hybrids are magic.' Bridge disparate fields.", "outcome_hint": "Interdisciplinary"},
            {"value": "B", "text": "'Need to pick a side.' Master one first.", "outcome_hint": "Disciplinary focus"}
        ]
    },
    {
        "id": "S8_TheEnvironment",
        "title": "Scenario 8: The Environment",
        "story": "Co-working space with varied zones (cafe, library, pods).",
        "options": [
            {"value": "A", "text": "Choose mode daily. Optimize output to mood.", "outcome_hint": "Dynamic environment"},
            {"value": "B", "text": "Too unpredictable. Decision fatigue. Prefer consistent home base.", "outcome_hint": "Stable environment"}
        ]
    },
    {
        "id": "S9_TheRole",
        "title": "Scenario 9: The Role",
        "story": "Consultant vs Employee.",
        "options": [
            {"value": "A", "text": "Consultant. New client every 3 months. Professional learner.", "outcome_hint": "Variety seeker"},
            {"value": "B", "text": "Employee. Long term deep expertise and relationships.", "outcome_hint": "Depth/Stability seeker"}
        ]
    },
    {
        "id": "S10_TheCuriosity",
        "title": "Scenario 10: The Curiosity",
        "story": "New revolutionary app.",
        "options": [
            {"value": "A", "text": "The UX (Social/Art). How it feels, human design.", "outcome_hint": "Human-centric"},
            {"value": "B", "text": "The Code (Logic/Math). How it works, rules.", "outcome_hint": "System-centric"}
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
