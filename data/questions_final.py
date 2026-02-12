
# Final Stream Assessment Questions (Phase 4)

# Stream Keys:
# PCM: Science (PCM)
# PCB: Science (PCB)
# COMM: Commerce
# ARTS: Arts/Humanities
# VOC: Vocational

# Section A: Aptitude (Correct Answer Logic)
# Scoring: If correct, add points to the mapped streams.
section_a_questions = [
    {
        "id": "FA1_Math",
        "question": "A manufacturing company needs to optimize its production line to reduce waste and increase output by 15%. They have collected data on current production rates, material costs, and labor hours. Which of the following skills would be most crucial for designing an effective solution?",
        "options": [
            {"value": "a", "text": "Analyzing historical documents and economic trends."},
            {"value": "b", "text": "Applying advanced statistical models and algorithmic thinking."},
            {"value": "c", "text": "Creating persuasive presentations and managing team dynamics."},
            {"value": "d", "text": "Designing and fabricating new mechanical components."}
        ],
        "correct_value": "b",
        "mapped_streams": ["PCM", "COMM"] 
    },
    {
        "id": "FA2_Science",
        "question": "You are tasked with designing a system to filter microplastics from ocean water. Which initial approach would be most effective?",
        "options": [
            {"value": "a", "text": "Studying the history of environmental conservation movements."},
            {"value": "b", "text": "Developing a marketing campaign to raise awareness about plastic pollution."},
            {"value": "c", "text": "Researching material science and fluid dynamics principles to design a physical filter."},
            {"value": "d", "text": "Organizing community clean-up drives and public speaking events."}
        ],
        "correct_value": "c",
        "mapped_streams": ["PCM", "PCB", "VOC"]
    },
    {
        "id": "FA3_SocialScience",
        "question": "A local government is debating whether to invest in a new public transportation system or allocate funds to improving existing road infrastructure. Which approach would be most effective in informing their decision?",
        "options": [
            {"value": "a", "text": "Conducting experiments to determine the optimal material for road construction."},
            {"value": "b", "text": "Analyzing population demographics, economic impacts, and historical urban development patterns."},
            {"value": "c", "text": "Writing a fictional story about future city life with advanced transportation."},
            {"value": "d", "text": "Developing a computer program to simulate traffic flow."}
        ],
        "correct_value": "b",
        "mapped_streams": ["ARTS", "COMM"]
    },
    {
        "id": "FA4_English",
        "question": "You need to present a complex scientific discovery to a general audience. Which skill is most vital for effective communication?",
        "options": [
            {"value": "a", "text": "Performing intricate mathematical calculations related to the discovery."},
            {"value": "b", "text": "Designing precise experimental protocols."},
            {"value": "c", "text": "Crafting clear, concise, and engaging narratives and explanations."},
            {"value": "d", "text": "Developing new laboratory equipment for further research."}
        ],
        "correct_value": "c",
        "mapped_streams": ["ARTS", "COMM"]
    },
    {
        "id": "FA5_Logic",
        "question": "In a sequence of numbers: 2, 6, 12, 20, 30, what is the next number?",
        "options": [
            {"value": "a", "text": "36"},
            {"value": "b", "text": "42"},
            {"value": "c", "text": "44"},
            {"value": "d", "text": "50"}
        ],
        "correct_value": "b", # 1x2, 2x3, 3x4, 4x5, 5x6, 6x7=42 OR +4, +6, +8, +10, +12
        "mapped_streams": ["PCM", "PCB", "COMM", "ARTS"] # Broad logic applies to all, helping general aptitude score
    }
]

# Section B: Interests (Preference Logic)
# Scoring: Each option maps to one primary stream.
section_b_questions = [
    {
        "id": "FB1_FreeTime",
        "question": "If you had an entire Saturday free, which activity would you most likely choose?",
        "options": [
            {"value": "a", "text": "Conducting a science experiment or building a complex model.", "stream": "PCM"}, # Could be PCB too, but usually model building is PCM/Eng
            {"value": "b", "text": "Managing your personal budget, researching stock markets, or planning a small business idea.", "stream": "COMM"},
            {"value": "c", "text": "Writing a story, painting, learning a new language, or visiting a museum.", "stream": "ARTS"},
            {"value": "d", "text": "Learning a practical skill like coding, carpentry, cooking, or graphic design.", "stream": "VOC"} # Coding could be PCM, but grouped with carpentry here implies vocational/skill
        ]
    },
    {
        "id": "FB2_NewTech",
        "question": "When you encounter a new gadget or technology, what is your first instinct?",
        "options": [
            {"value": "a", "text": "To understand how it works internally and its underlying principles.", "stream": "PCM"},
            {"value": "b", "text": "To assess its market value and potential for profit.", "stream": "COMM"},
            {"value": "c", "text": "To explore its aesthetic design and user experience.", "stream": "ARTS"},
            {"value": "d", "text": "To immediately try to use it for a practical task or modify it.", "stream": "VOC"}
        ]
    },
    {
        "id": "FB3_Media",
        "question": "Which type of book or documentary do you find most engaging?",
        "options": [
            {"value": "a", "text": "About scientific discoveries, space exploration, or the human body.", "stream": "PCB"}, # "Human body" pulls toward PCB/Bio
            {"value": "b", "text": "About business strategies, economic history, or biographies of entrepreneurs.", "stream": "COMM"},
            {"value": "c", "text": "About historical events, philosophical debates, or literary analyses.", "stream": "ARTS"},
            {"value": "d", "text": "About how things are made, practical guides, or skill-based tutorials.", "stream": "VOC"}
        ]
    },
    {
        "id": "FB4_WorldProblem",
        "question": "Imagine a world problem you want to solve. Which aspect would you be most drawn to?",
        "options": [
            {"value": "a", "text": "Inventing new technologies or finding scientific cures.", "stream": "PCB"}, # Cures = Bio
            {"value": "b", "text": "Developing sustainable economic models or efficient resource allocation.", "stream": "COMM"},
            {"value": "c", "text": "Understanding societal causes, promoting social justice, or communicating solutions.", "stream": "ARTS"},
            {"value": "d", "text": "Implementing practical solutions on the ground or training others in essential skills.", "stream": "VOC"}
        ]
    },
    {
        "id": "FB5_Activity",
        "question": "Which extracurricular activity genuinely excites you the most?",
        "options": [
            {"value": "a", "text": "Science club, robotics, or coding competitions.", "stream": "PCM"},
            {"value": "b", "text": "Debate club, student council, or managing school events.", "stream": "COMM"},
            {"value": "c", "text": "Drama club, school newspaper, creative writing, or art classes.", "stream": "ARTS"},
            {"value": "d", "text": "Technical workshops, vocational training, or community service projects involving practical skills.", "stream": "VOC"}
        ]
    }
]

# Section C: Personality (Learning Style Logic)
section_c_questions = [
    {
        "id": "FC1_Learning",
        "question": "When learning something new, what approach do you prefer?",
        "options": [
            {"value": "a", "text": "Hands-on experimentation and observation.", "stream": "PCB"}, # Observation is key in Bio
            {"value": "b", "text": "Analyzing data, case studies, and financial reports.", "stream": "COMM"},
            {"value": "c", "text": "Reading, discussing theories, and writing essays.", "stream": "ARTS"},
            {"value": "d", "text": "Practicing skills repeatedly and building prototypes.", "stream": "VOC"} # Prototypes often Eng/Voc
        ]
    },
    {
        "id": "FC2_TeamRole",
        "question": "You are part of a team project. What role do you naturally gravitate towards?",
        "options": [
            {"value": "a", "text": "The researcher, gathering facts and testing hypotheses.", "stream": "PCM"},
            {"value": "b", "text": "The planner, organizing tasks and managing resources.", "stream": "COMM"},
            {"value": "c", "text": "The communicator, presenting ideas and facilitating discussions.", "stream": "ARTS"},
            {"value": "d", "text": "The doer, focusing on implementing the practical aspects.", "stream": "VOC"}
        ]
    },
    {
        "id": "FC3_Feedback",
        "question": "How do you prefer to receive feedback on your work?",
        "options": [
            {"value": "a", "text": "Detailed analysis of data and results, focusing on objectivity.", "stream": "PCM"},
            {"value": "b", "text": "Constructive criticism on efficiency, cost-effectiveness, and strategy.", "stream": "COMM"},
            {"value": "c", "text": "Thoughtful comments on creativity, clarity, and persuasive power.", "stream": "ARTS"},
            {"value": "d", "text": "Guidance on improving practical techniques and hands-on application.", "stream": "VOC"}
        ]
    },
    {
        "id": "FC4_Decision",
        "question": "When making important decisions, you tend to rely more on:",
        "options": [
            {"value": "a", "text": "Objective data and logical reasoning.", "stream": "PCM"},
            {"value": "b", "text": "Cost-benefit analysis and strategic planning.", "stream": "COMM"},
            {"value": "c", "text": "Intuition, empathy, and ethical considerations.", "stream": "ARTS"},
            {"value": "d", "text": "Practical feasibility and immediate impact.", "stream": "VOC"}
        ]
    },
    {
        "id": "FC5_SubjectType",
        "question": "Do you enjoy subjects that have clear-cut answers and established formulas, or those that encourage open-ended interpretation and creative expression?",
        "options": [
            {"value": "a", "text": "Clear-cut answers and formulas.", "stream": "PCM"},
            {"value": "b", "text": "A balance of both, with a focus on practical application.", "stream": "COMM"}, # Comm is often applied math/rules
            {"value": "c", "text": "Open-ended interpretation and creative expression.", "stream": "ARTS"},
            {"value": "d", "text": "Hands-on problem-solving with tangible results.", "stream": "VOC"}
        ]
    }
]

# Section D: Scenarios
section_d_questions = [
    {
        "id": "FD1_Charity",
        "question": "Your school wants to organize a charity event. Which aspect would you be most excited to contribute to?",
        "options": [
            {"value": "a", "text": "Designing a scientific exhibit to raise awareness about a health issue.", "stream": "PCB"},
            {"value": "b", "text": "Managing the budget, fundraising, and logistics of the event.", "stream": "COMM"},
            {"value": "c", "text": "Creating promotional materials (posters, social media content) and writing speeches.", "stream": "ARTS"},
            {"value": "d", "text": "Building and setting up the physical infrastructure for the event.", "stream": "VOC"}
        ]
    },
    {
        "id": "FD2_Plant",
        "question": "You discover a new species of plant in your backyard. What would be your immediate next step?",
        "options": [
            {"value": "a", "text": "Collecting samples, observing its characteristics, and researching similar species.", "stream": "PCB"},
            {"value": "b", "text": "Considering its potential commercial value or environmental impact for local regulations.", "stream": "COMM"},
            {"value": "c", "text": "Writing a detailed description of its features and perhaps a poem inspired by its beauty.", "stream": "ARTS"},
            {"value": "d", "text": "Attempting to cultivate it or extracting its compounds for practical uses.", "stream": "VOC"}
        ]
    },
    {
        "id": "FD3_History",
        "question": "A complex historical event is being discussed in class. What part of the discussion would captivate you the most?",
        "options": [
            {"value": "a", "text": "The technological advancements or scientific discoveries that influenced the era.", "stream": "PCM"},
            {"value": "b", "text": "The economic factors, trade routes, and political power struggles.", "stream": "COMM"},
            {"value": "c", "text": "The personal stories, cultural shifts, and philosophical ideas of the time.", "stream": "ARTS"},
            {"value": "d", "text": "How people adapted practically to the challenges of that period.", "stream": "VOC"}
        ]
    },
    {
        "id": "FD4_Project",
        "question": "You have to choose a project for a school fair. Which project idea would you find most appealing?",
        "options": [
            {"value": "a", "text": "Building a functioning robot arm or demonstrating a chemical reaction.", "stream": "PCM"},
            {"value": "b", "text": "Creating a business plan for a new product or analyzing market trends.", "stream": "COMM"},
            {"value": "c", "text": "Producing a short film, designing a fashion collection, or performing a monologue.", "stream": "ARTS"},
            {"value": "d", "text": "Restoring an old piece of furniture or coding a simple mobile application.", "stream": "VOC"}
        ]
    },
    {
        "id": "FD5_HealthyEating",
        "question": "You are trying to persuade your friends to adopt a new, healthier eating habit. What would be your primary strategy?",
        "options": [
            {"value": "a", "text": "Explaining the scientific benefits of the diet and presenting nutritional data.", "stream": "PCB"},
            {"value": "b", "text": "Calculating the cost savings and long-term economic advantages of healthy eating.", "stream": "COMM"},
            {"value": "c", "text": "Sharing compelling stories, creating appealing recipes, and discussing the cultural aspects of food.", "stream": "ARTS"},
            {"value": "d", "text": "Demonstrating how to prepare healthy meals efficiently and practically.", "stream": "VOC"}
        ]
    },
    {
        "id": "FD6_Mentoring",
        "question": "You are given an opportunity to mentor a younger student. What would you focus on?",
        "options": [
            {"value": "a", "text": "Helping them grasp complex scientific or mathematical concepts.", "stream": "PCM"},
            {"value": "b", "text": "Teaching them organizational skills, time management, and financial literacy.", "stream": "COMM"},
            {"value": "c", "text": "Encouraging critical thinking, creative expression, and effective communication.", "stream": "ARTS"},
            {"value": "d", "text": "Showing them how to perform practical tasks or use specific tools.", "stream": "VOC"}
        ]
    },
    {
        "id": "FD7_EthicalDilemma",
        "question": "A new ethical dilemma arises from a technological advancement (e.g., AI in healthcare). What is your main concern?",
        "options": [
            {"value": "a", "text": "The technical feasibility and safety of the technology itself.", "stream": "PCM"},
            {"value": "b", "text": "The economic implications and regulatory challenges for businesses.", "stream": "COMM"},
            {"value": "c", "text": "The moral philosophical arguments, societal impact, and human rights considerations.", "stream": "ARTS"},
            {"value": "d", "text": "The practical steps needed to implement or mitigate the technology's effects.", "stream": "VOC"}
        ]
    },
    {
        "id": "FD8_Trip",
        "question": "You are planning a trip with friends. What role do you enjoy the most?",
        "options": [
            {"value": "a", "text": "Researching the best travel routes, scientific attractions, or optimal packing techniques.", "stream": "PCM"}, # Optimization/Science
            {"value": "b", "text": "Budgeting, finding deals, and managing the overall expenses.", "stream": "COMM"},
            {"value": "c", "text": "Designing the itinerary, documenting the experience (photos, writing), and choosing cultural sites.", "stream": "ARTS"},
            {"value": "d", "text": "Handling the practical arrangements, like booking transportation or setting up campsites.", "stream": "VOC"}
        ]
    },
    {
        "id": "FD9_Puzzle",
        "question": "A challenging puzzle needs to be solved. What approach do you instinctively take?",
        "options": [
            {"value": "a", "text": "Breaking it down into logical steps and applying systematic problem-solving methods.", "stream": "PCM"},
            {"value": "b", "text": "Considering the most efficient way to solve it with minimal resources, even if unconventional.", "stream": "COMM"},
            {"value": "c", "text": "Thinking outside the box, exploring multiple interpretations, and seeking creative solutions.", "stream": "ARTS"},
            {"value": "d", "text": "Trying different physical manipulations or practical tools until a solution emerges.", "stream": "VOC"}
        ]
    },
    {
        "id": "FD10_ProductReview",
        "question": "You are asked to review a new product. What aspects would you prioritize in your evaluation?",
        "options": [
            {"value": "a", "text": "Its technical specifications, performance data, and scientific innovations.", "stream": "PCM"},
            {"value": "b", "text": "Its market viability, pricing strategy, and potential return on investment.", "stream": "COMM"},
            {"value": "c", "text": "Its user experience, aesthetic appeal, and the story it tells.", "stream": "ARTS"},
            {"value": "d", "text": "Its durability, ease of use, and practical functionality.", "stream": "VOC"}
        ]
    }
]

# Combined List for Template Iteration
all_questions = {
    "section_a": {"title": "Section A: Aptitude", "questions": section_a_questions},
    "section_b": {"title": "Section B: Interests", "questions": section_b_questions},
    "section_c": {"title": "Section C: Personality", "questions": section_c_questions},
    "section_d": {"title": "Section D: Scenarios", "questions": section_d_questions}
}
