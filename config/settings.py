"""All static configuration in one place: fields, dimensions, model name,
fallback questions, and the small numeric constants that used to be
scattered inline throughout the old single-file app."""

FIELDS = {
    "AI & Machine Learning": {
        "keywords": ["machine learning", "deep learning", "neural network",
                     "artificial intelligence", "nlp", "computer vision", "data science"],
        "focus": {
            "Programming": "writing/reading Python code for data manipulation and ML workflows (e.g. NumPy/Pandas operations, simple functions, list/array logic)",
            "Aptitude": "logical, probability, and statistical reasoning relevant to machine learning",
            "Technical": "core ML/AI concepts (supervised vs unsupervised learning, overfitting, neural network basics, model evaluation)",
            "Problem Solving": "diagnosing realistic ML workflow problems (e.g. why a model is overfitting, choosing the right approach for a dataset)",
            "Communication": "explaining technical ML concepts and results clearly to a non-technical audience",
        },
    },
    "Web Development": {
        "keywords": ["web development", "javascript", "html", "css", "frontend", "backend", "react", "full stack"],
        "focus": {
            "Programming": "reading/reasoning about JavaScript, HTML, or CSS code snippets and common web programming logic",
            "Aptitude": "logical reasoning applied to structuring UI flows, sequencing, and debugging logic",
            "Technical": "core web development concepts (HTTP requests, REST APIs, client-server model, responsive design, browser rendering)",
            "Problem Solving": "diagnosing bugs or performance issues in a realistic web application scenario",
            "Communication": "writing clear technical documentation or explaining a bug/feature to a teammate or client",
        },
    },
    "Data Science": {
        "keywords": ["data science", "data analysis", "statistics", "data visualization", "sql", "pandas"],
        "focus": {
            "Programming": "writing/reading Python or SQL code for data analysis and transformation",
            "Aptitude": "statistical and numerical reasoning (interpreting averages, distributions, correlation vs causation)",
            "Technical": "core data science concepts (data cleaning, visualization choices, statistical significance, common pitfalls)",
            "Problem Solving": "reasoning through a realistic messy-data or analysis-design scenario",
            "Communication": "presenting a data insight clearly and accurately to a non-technical stakeholder",
        },
    },
    "Cybersecurity": {
        "keywords": ["cybersecurity", "network security", "information security", "ethical hacking", "cryptography"],
        "focus": {
            "Programming": "reading/reasoning about scripts related to security tasks (e.g. spotting insecure code patterns)",
            "Aptitude": "logical reasoning applied to identifying anomalies, patterns, or vulnerabilities",
            "Technical": "core cybersecurity concepts (encryption basics, phishing, firewalls, authentication vs authorization)",
            "Problem Solving": "diagnosing a realistic security incident or vulnerability scenario",
            "Communication": "explaining a security risk and recommended action clearly to a non-technical manager",
        },
    },
    "Mobile App Development": {
        "keywords": ["mobile development", "android", "ios", "swift", "kotlin", "flutter", "app development"],
        "focus": {
            "Programming": "reading/reasoning about mobile app code logic (Kotlin/Swift/Flutter-style snippets, state handling)",
            "Aptitude": "logical reasoning applied to UI flow sequencing and app state logic",
            "Technical": "core mobile development concepts (native vs cross-platform, app lifecycle, local storage vs API calls)",
            "Problem Solving": "diagnosing a realistic mobile app bug or performance/UX issue",
            "Communication": "explaining a feature tradeoff or bug clearly to a product manager or teammate",
        },
    },
}

DIMENSIONS = ["Programming", "Aptitude", "Technical", "Problem Solving", "Communication"]

MISTRAL_MODEL = "open-mistral-7b"

# Score cutoffs for Low / Medium / High competency labels.
SCORE_THRESHOLDS = {
    "low": 40,    # below this -> "Low"
    "medium": 70, # below this (and >= low) -> "Medium"; at/above -> "High"
}

DIFFICULTY_SPLIT = {'easy': 2, 'medium': 2, 'hard': 2}
N_PER_DIMENSION = sum(DIFFICULTY_SPLIT.values())
TOP_N_RECOMMENDATIONS = 5

# OFFLINE FALLBACK — used only if no API key is set or a generation call
# fails after retries, so the app never crashes mid-demo.
FALLBACK_QUESTIONS = {
    'Programming': [
        {'question': "Which keyword is used to define a function in Python?",
         'options': ["def", "func", "function", "lambda"], 'correct_answer': 0, 'difficulty': 'easy'},
        {'question': "Which data structure follows First-In-First-Out (FIFO) order?",
         'options': ["Stack", "Queue", "Array", "Tree"], 'correct_answer': 1, 'difficulty': 'easy'},
        {'question': "What will `len([1, 2, [3, 4]])` return in Python?",
         'options': ["3", "4", "2", "Error"], 'correct_answer': 0, 'difficulty': 'medium'},
        {'question': "Which of these has O(log n) average search time on a sorted array?",
         'options': ["Linear Search", "Binary Search", "Bubble Sort", "Insertion Sort"], 'correct_answer': 1, 'difficulty': 'medium'},
        {'question': "What does this code print?\n\nx = [1, 2, 3]\ny = x\ny.append(4)\nprint(len(x))",
         'options': ["3", "4", "Error", "None"], 'correct_answer': 1, 'difficulty': 'hard'},
        {'question': "What is the average time complexity of inserting into a Python dictionary?",
         'options': ["O(1)", "O(n)", "O(log n)", "O(n^2)"], 'correct_answer': 0, 'difficulty': 'hard'},
    ],
    'Aptitude': [
        {'question': "What number comes next: 3, 6, 12, 24, ?",
         'options': ["36", "48", "30", "42"], 'correct_answer': 1, 'difficulty': 'easy'},
        {'question': "Which number does NOT belong in this set: 3, 5, 9, 11, 13?",
         'options': ["3", "5", "9", "13"], 'correct_answer': 2, 'difficulty': 'easy'},
        {'question': "If all Zorbs are Blips, and all Blips are Corns, which statement must be true?",
         'options': ["All Zorbs are Corns", "All Corns are Zorbs", "No Zorbs are Corns", "Cannot be determined"], 'correct_answer': 0, 'difficulty': 'medium'},
        {'question': "A clock shows 3:15. What is the approximate angle between the hour and minute hands?",
         'options': ["0°", "7.5°", "15°", "30°"], 'correct_answer': 1, 'difficulty': 'medium'},
        {'question': "What number comes next in the series: 2, 6, 12, 20, 30, ?",
         'options': ["36", "42", "40", "38"], 'correct_answer': 1, 'difficulty': 'hard'},
        {'question': "Three people can complete a task in 6 hours. How many hours would it take 2 people working at the same rate?",
         'options': ["4", "9", "8", "12"], 'correct_answer': 1, 'difficulty': 'hard'},
    ],
    'Technical': [
        {'question': "What does a URL primarily do?",
         'options': ["Encrypts a file", "Identifies a resource's location on the web", "Compiles source code", "Stores a password"], 'correct_answer': 1, 'difficulty': 'easy'},
        {'question': "What does 'API' stand for?",
         'options': ["Application Programming Interface", "Automated Program Installer", "Applied Programming Instruction", "Application Process Integration"], 'correct_answer': 0, 'difficulty': 'easy'},
        {'question': "Which of these is a NoSQL database?",
         'options': ["MySQL", "PostgreSQL", "MongoDB", "SQLite"], 'correct_answer': 2, 'difficulty': 'medium'},
        {'question': "What is the main purpose of a version control system like Git?",
         'options': ["Compiling code faster", "Tracking changes and enabling collaboration", "Encrypting source code", "Running automated tests"], 'correct_answer': 1, 'difficulty': 'medium'},
        {'question': "In networking, what does 'DNS' primarily do?",
         'options': ["Encrypts network traffic", "Translates domain names into IP addresses", "Assigns MAC addresses", "Compresses data packets"], 'correct_answer': 1, 'difficulty': 'hard'},
        {'question': "What is the main advantage of using a load balancer in a distributed system?",
         'options': ["Reduces code complexity", "Distributes traffic across multiple servers to improve reliability", "Encrypts all data", "Replaces the need for a database"], 'correct_answer': 1, 'difficulty': 'hard'},
    ],
    'Problem Solving': [
        {'question': "A train travels 60 miles in 45 minutes. What is its speed in mph?",
         'options': ["60 mph", "75 mph", "80 mph", "90 mph"], 'correct_answer': 2, 'difficulty': 'easy'},
        {'question': "A bat and a ball cost $1.10 total. The bat costs $1.00 more than the ball. How much does the ball cost?",
         'options': ["$0.10", "$0.05", "$1.00", "$0.15"], 'correct_answer': 1, 'difficulty': 'easy'},
        {'question': "You have 8 identical-looking balls, one heavier. Using a balance scale, what's the minimum number of weighings to guarantee finding it?",
         'options': ["1", "2", "3", "4"], 'correct_answer': 1, 'difficulty': 'medium'},
        {'question': "A recipe for 4 people needs 2 cups of rice. How many cups are needed for 10 people?",
         'options': ["4", "5", "6", "8"], 'correct_answer': 1, 'difficulty': 'medium'},
        {'question': "Three switches outside a room control three bulbs inside. You can flip switches freely but enter the room only once. How do you determine which switch controls which bulb?",
         'options': ["It's impossible", "Turn on switch 1, wait, turn it off, turn on switch 2, then enter and check bulb heat and state", "Turn each switch on one at a time and peek under the door", "Use a mirror to see inside"], 'correct_answer': 1, 'difficulty': 'hard'},
        {'question': "You have two ropes that each burn in exactly 60 minutes but burn unevenly. How can you measure 45 minutes?",
         'options': ["Burn one rope from both ends and the other from one end simultaneously; when the first finishes, light the other end of the second", "It's impossible without a clock", "Burn both ropes from one end at the same time", "Cut both ropes in half and burn all four ends"], 'correct_answer': 0, 'difficulty': 'hard'},
    ],
    'Communication': [
        {'question': "Which sentence is written in active voice?",
         'options': ["The report was completed by the team.", "The team completed the report.", "The report has been completed.", "Completion was done."], 'correct_answer': 1, 'difficulty': 'easy'},
        {'question': "Which is the best email subject line for requesting urgent feedback by end of day?",
         'options': ["Hey", "Document", "Feedback Needed by 5 PM Today – [Document Name]", "FYI"], 'correct_answer': 2, 'difficulty': 'easy'},
        {'question': "Which is the clearest, most professional way to decline a meeting?",
         'options': ["Can't make it, sorry.", "I'm unable to attend this meeting due to a scheduling conflict — could we reschedule?", "Not going, busy.", "Meeting doesn't work for me lol"], 'correct_answer': 1, 'difficulty': 'medium'},
        {'question': "What is the main risk of using excessive jargon with a general audience?",
         'options': ["It makes you sound smarter", "It saves time", "It can confuse or alienate the audience", "It has no effect"], 'correct_answer': 2, 'difficulty': 'medium'},
        {'question': "A colleague's report contains a factual error. Which is the best way to raise it?",
         'options': ["Point it out publicly in the team meeting so everyone learns from it", "Privately mention the specific error, explain why it matters, and offer to help fix it", "Ignore it since it's not your responsibility", "Rewrite the whole report yourself without telling them"], 'correct_answer': 1, 'difficulty': 'hard'},
        {'question': "You must tell a client about a missed deadline. What is the most professional approach?",
         'options': ["Delay telling them until the last possible moment", "Proactively inform them early, explain the cause, and propose a revised plan", "Blame a teammate to preserve the relationship", "Avoid specifics and hope they don't notice"], 'correct_answer': 1, 'difficulty': 'hard'},
    ],
}


# UI color palette
COLOR_PRIMARY = "#ABC270"         # green -- primary actions, High level, course links
COLOR_ACCENT_YELLOW = "#FEC868"   # Medium level, skills, progress bar
COLOR_ACCENT_ORANGE = "#FDA769"   # Low level, secondary accents
COLOR_BUTTON_TEXT = "#463C33"     # text on buttons -- constant in BOTH light and dark mode

LIGHT_MODE = {"background": "#FFFFFF", "text": "#463C33"}
DARK_MODE = {"background": "#000000", "text": "#FFFFFF"}