CAREER_ROLES = {
    "Data Analyst": [
        "Python",
        "SQL",
        "Data Analysis",
        "Data Visualization",
        "Statistics",
        "Excel",
        "Power BI",
    ],
    "Web Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Git",
        "Responsive Design",
    ],
    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Statistics",
        "Deep Learning",
        "TensorFlow",
        "Data Structures",
    ],
    "Backend Developer": [
        "Python",
        "SQL",
        "APIs",
        "Flask",
        "Git",
        "Data Structures",
    ],
    "Software Developer": [
        "Programming",
        "Data Structures",
        "Algorithms",
        "Java",
        "C++",
        "Git",
    ],
    "Frontend Developer": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Responsive Design",
        "Git",
    ],
}

LEARNING_GUIDANCE = {
    "Python": {
        "topics": ["Python basics", "Functions and OOP", "Projects with APIs"],
        "start": "Start with Python syntax and small scripts, then solve easy automation and data tasks.",
        "how_to_learn": "Spend the first week on basics, the second on problem solving, and then build mini projects.",
        "daily_minutes": 60,
        "practice_sites": ["HackerRank", "Exercism", "Kaggle"],
        "links": [
            "https://docs.python.org/3/tutorial/",
            "https://www.kaggle.com/learn/python",
            "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
        ],
    },
    "SQL": {
        "topics": ["Queries", "Joins", "Aggregations and case studies"],
        "start": "Start by learning SELECT, WHERE, GROUP BY, and JOIN using sample datasets.",
        "how_to_learn": "Practice one query pattern each day and review real reporting questions.",
        "daily_minutes": 45,
        "practice_sites": ["SQLBolt", "Mode SQL Tutorial", "StrataScratch"],
        "links": [
            "https://www.w3schools.com/sql/",
            "https://www.sqlbolt.com/",
            "https://www.youtube.com/watch?v=HXV3zeQKqGY",
        ],
    },
    "Data Analysis": {
        "topics": ["Cleaning data", "EDA", "Insight storytelling"],
        "start": "Start with spreadsheets and pandas on small CSV files.",
        "how_to_learn": "Alternate between learning one concept and applying it to a dataset.",
        "daily_minutes": 60,
        "practice_sites": ["Kaggle", "DataCamp Workspace", "Maven Analytics"],
        "links": [
            "https://www.kaggle.com/learn/pandas",
            "https://pandas.pydata.org/docs/getting_started/index.html",
            "https://www.youtube.com/watch?v=r-uOLxNrNk8",
        ],
    },
    "Data Visualization": {
        "topics": ["Chart types", "Dashboards", "Storytelling"],
        "start": "Start with bar, line, and scatter charts before building dashboards.",
        "how_to_learn": "Create one visualization every day from a small dataset.",
        "daily_minutes": 40,
        "practice_sites": ["Tableau Public", "Power BI Learn", "Kaggle"],
        "links": [
            "https://www.tableau.com/learn/training",
            "https://www.chartjs.org/docs/latest/",
            "https://www.youtube.com/watch?v=aHaOIvR00So",
        ],
    },
    "Statistics": {
        "topics": ["Descriptive statistics", "Probability", "Hypothesis testing"],
        "start": "Start with mean, median, variance, and probability basics.",
        "how_to_learn": "Pair each concept with 3-5 worked problems.",
        "daily_minutes": 45,
        "practice_sites": ["Khan Academy", "Brilliant", "Stat Trek"],
        "links": [
            "https://www.khanacademy.org/math/statistics-probability",
            "https://openstax.org/details/books/introductory-statistics",
            "https://www.youtube.com/watch?v=xxpc-HPKN28",
        ],
    },
    "Machine Learning": {
        "topics": ["Supervised learning", "Evaluation metrics", "Feature engineering"],
        "start": "Start with regression and classification using scikit-learn.",
        "how_to_learn": "Learn one model family at a time and validate it on a small dataset.",
        "daily_minutes": 75,
        "practice_sites": ["Kaggle", "Google Colab", "DrivenData"],
        "links": [
            "https://developers.google.com/machine-learning/crash-course",
            "https://scikit-learn.org/stable/",
            "https://www.youtube.com/watch?v=GwIo3gDZCVQ",
        ],
    },
    "Deep Learning": {
        "topics": ["Neural networks", "CNNs", "Model tuning"],
        "start": "Start with perceptrons and dense networks before moving to CNNs.",
        "how_to_learn": "Mix theory reading with notebook-based experiments.",
        "daily_minutes": 75,
        "practice_sites": ["Kaggle", "Google Colab", "Papers with Code"],
        "links": [
            "https://www.deeplearning.ai/courses/",
            "https://www.tensorflow.org/learn",
            "https://www.youtube.com/watch?v=aircAruvnKk",
        ],
    },
    "TensorFlow": {
        "topics": ["TensorFlow basics", "Keras models", "Model deployment"],
        "start": "Start with TensorFlow tensors and Keras Sequential models.",
        "how_to_learn": "Build one notebook model, then iterate with better metrics and callbacks.",
        "daily_minutes": 60,
        "practice_sites": ["Google Colab", "Kaggle", "TensorFlow Tutorials"],
        "links": [
            "https://www.tensorflow.org/tutorials",
            "https://www.coursera.org/specializations/tensorflow-in-practice",
            "https://www.youtube.com/watch?v=tPYj3fFJGjk",
        ],
    },
    "Programming": {
        "topics": ["Core logic", "Functions", "Problem solving"],
        "start": "Start with variables, loops, and functions in one language.",
        "how_to_learn": "Write small programs every day and review mistakes.",
        "daily_minutes": 45,
        "practice_sites": ["HackerRank", "LeetCode", "Exercism"],
        "links": [
            "https://leetcode.com/",
            "https://www.hackerrank.com/domains/tutorials/10-days-of-javascript",
            "https://www.youtube.com/watch?v=zOjov-2OZ0E",
        ],
    },
    "Data Structures": {
        "topics": ["Arrays and strings", "Trees and graphs", "Hashing"],
        "start": "Start with arrays, stacks, queues, and hash maps.",
        "how_to_learn": "Study one structure, then solve 2-3 questions using it.",
        "daily_minutes": 60,
        "practice_sites": ["LeetCode", "GeeksforGeeks", "Visualgo"],
        "links": [
            "https://www.geeksforgeeks.org/data-structures/",
            "https://visualgo.net/en",
            "https://www.youtube.com/watch?v=RBSGKlAvoiM",
        ],
    },
    "Algorithms": {
        "topics": ["Sorting", "Searching", "Dynamic programming"],
        "start": "Start with sorting and binary search before moving to recursion and DP.",
        "how_to_learn": "Practice patterns repeatedly and revisit missed questions.",
        "daily_minutes": 60,
        "practice_sites": ["LeetCode", "Codeforces", "NeetCode"],
        "links": [
            "https://cp-algorithms.com/",
            "https://neetcode.io/roadmap",
            "https://www.youtube.com/watch?v=8hly31xKli0",
        ],
    },
    "Java": {
        "topics": ["Syntax", "Collections", "OOP and backend basics"],
        "start": "Start with classes, objects, loops, and collections.",
        "how_to_learn": "Build console apps first, then simple backend services.",
        "daily_minutes": 60,
        "practice_sites": ["HackerRank", "CodeChef", "LeetCode"],
        "links": [
            "https://dev.java/learn/",
            "https://spring.io/guides",
            "https://www.youtube.com/watch?v=eIrMbAQSU34",
        ],
    },
    "C++": {
        "topics": ["Syntax", "STL", "Pointers and OOP"],
        "start": "Start with syntax and STL containers before tackling pointers deeply.",
        "how_to_learn": "Practice daily with short competitive-style problems.",
        "daily_minutes": 60,
        "practice_sites": ["CodeChef", "LeetCode", "GeeksforGeeks"],
        "links": [
            "https://www.learncpp.com/",
            "https://cplusplus.com/doc/tutorial/",
            "https://www.youtube.com/watch?v=vLnPwxZdW4Y",
        ],
    },
    "HTML": {
        "topics": ["Semantic markup", "Forms", "Accessibility"],
        "start": "Start with page structure, headings, forms, and semantic tags.",
        "how_to_learn": "Rebuild small page layouts and inspect good examples.",
        "daily_minutes": 30,
        "practice_sites": ["freeCodeCamp", "Frontend Mentor", "MDN"],
        "links": [
            "https://developer.mozilla.org/en-US/docs/Web/HTML",
            "https://www.freecodecamp.org/learn/2022/responsive-web-design/",
            "https://www.youtube.com/watch?v=qz0aGYrrlhU",
        ],
    },
    "CSS": {
        "topics": ["Selectors", "Flexbox and Grid", "Responsive design"],
        "start": "Start with selectors, spacing, and layout fundamentals.",
        "how_to_learn": "Style one component a day and test it on mobile and desktop.",
        "daily_minutes": 35,
        "practice_sites": ["Frontend Mentor", "CSSBattle", "MDN"],
        "links": [
            "https://developer.mozilla.org/en-US/docs/Web/CSS",
            "https://css-tricks.com/snippets/css/a-guide-to-flexbox/",
            "https://www.youtube.com/watch?v=1PnVor36_40",
        ],
    },
    "JavaScript": {
        "topics": ["Core syntax", "DOM", "Async programming"],
        "start": "Start with variables, arrays, functions, and DOM events.",
        "how_to_learn": "Learn one concept, then apply it in a browser mini project.",
        "daily_minutes": 50,
        "practice_sites": ["freeCodeCamp", "Frontend Mentor", "Codewars"],
        "links": [
            "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide",
            "https://javascript.info/",
            "https://www.youtube.com/watch?v=PkZNo7MFNFg",
        ],
    },
    "Excel": {
        "topics": ["Formulas", "Pivot tables", "Dashboards"],
        "start": "Start with formulas, filters, and tables on simple sheets.",
        "how_to_learn": "Recreate a mini dashboard from sample data.",
        "daily_minutes": 30,
        "practice_sites": ["Excel Practice Online", "GCFGlobal", "Kaggle"],
        "links": [
            "https://support.microsoft.com/excel",
            "https://edu.gcfglobal.org/en/excel/",
            "https://www.youtube.com/watch?v=Vl0H-qTclOg",
        ],
    },
    "Power BI": {
        "topics": ["Data loading", "DAX basics", "Dashboards"],
        "start": "Start with importing CSV files and making simple visuals.",
        "how_to_learn": "Build one dashboard a week and improve it iteratively.",
        "daily_minutes": 40,
        "practice_sites": ["Microsoft Learn", "Maven Analytics", "Kaggle"],
        "links": [
            "https://learn.microsoft.com/power-bi/",
            "https://www.youtube.com/watch?v=AGrl-H87pRU",
            "https://www.sqlbi.com/training/",
        ],
    },
    "React": {
        "topics": ["Components", "State", "Forms and API calls"],
        "start": "Start with components, props, and state management basics.",
        "how_to_learn": "Build small UI sections first, then a complete mini app.",
        "daily_minutes": 50,
        "practice_sites": ["Frontend Mentor", "Scrimba", "freeCodeCamp"],
        "links": [
            "https://react.dev/learn",
            "https://www.freecodecamp.org/news/react-beginner-handbook/",
            "https://www.youtube.com/watch?v=bMknfKXIFA8",
        ],
    },
    "Git": {
        "topics": ["Commits", "Branches", "Merge workflow"],
        "start": "Start with init, add, commit, push, and pull.",
        "how_to_learn": "Use Git in every small project so the commands become natural.",
        "daily_minutes": 20,
        "practice_sites": ["Learn Git Branching", "GitHub Skills", "Atlassian Tutorials"],
        "links": [
            "https://learngitbranching.js.org/",
            "https://skills.github.com/",
            "https://www.youtube.com/watch?v=RGOj5yH7evk",
        ],
    },
    "Responsive Design": {
        "topics": ["Mobile-first layouts", "Breakpoints", "Flexible components"],
        "start": "Start by designing one layout for mobile and then scaling upward.",
        "how_to_learn": "Review one UI and improve its responsiveness each day.",
        "daily_minutes": 30,
        "practice_sites": ["Frontend Mentor", "MDN", "CSSBattle"],
        "links": [
            "https://web.dev/responsive-web-design-basics/",
            "https://developer.mozilla.org/en-US/docs/Learn/CSS/CSS_layout/Responsive_Design",
            "https://www.youtube.com/watch?v=srvUrASNj0s",
        ],
    },
    "APIs": {
        "topics": ["REST basics", "HTTP methods", "JSON responses"],
        "start": "Start with GET and POST requests using Postman and a simple Flask app.",
        "how_to_learn": "Read API docs and build one endpoint or client request every day.",
        "daily_minutes": 40,
        "practice_sites": ["Postman Student Expert", "RapidAPI", "freeCodeCamp"],
        "links": [
            "https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Client-side_web_APIs/Introduction",
            "https://www.postman.com/student-programs/student-expert/",
            "https://www.youtube.com/watch?v=WXsD0ZgxjRw",
        ],
    },
    "Flask": {
        "topics": ["Routing", "Templates", "Forms and database basics"],
        "start": "Start with a hello-world route, then add forms and template rendering.",
        "how_to_learn": "Build one small Flask feature at a time and connect it to SQLite.",
        "daily_minutes": 40,
        "practice_sites": ["Flask Docs", "freeCodeCamp", "Real Python"],
        "links": [
            "https://flask.palletsprojects.com/",
            "https://realpython.com/tutorials/flask/",
            "https://www.youtube.com/watch?v=Z1RJmh_OqeA",
        ],
    },
}


def default_learning_guidance(skill):
    return {
        "topics": ["Foundational concepts", "Hands-on exercises", "Applied mini projects"],
        "start": f"Start with the basic concepts of {skill} and simple examples.",
        "how_to_learn": f"Learn {skill} through short lessons, practice tasks, and one small project.",
        "daily_minutes": 30,
        "practice_sites": ["YouTube practice playlists", "Kaggle", "HackerRank"],
        "links": [
            "https://www.coursera.org/",
            "https://www.edx.org/",
            "https://www.youtube.com/",
        ],
    }


def calculate_match_score(student_skills, required_skills):
    required_set = set(required_skills)
    student_set = set(student_skills)
    matched = sorted(list(required_set.intersection(student_set)))
    if not required_set:
        return matched, 0.0
    score = round((len(matched) / len(required_set)) * 100, 2)
    return matched, score


def build_recommendations(student_skills, roles):
    recs = []
    for role, required in roles.items():
        matched, score = calculate_match_score(student_skills, required)
        missing = sorted(list(set(required) - set(matched)))
        if matched:
            reason = (
                f"Your resume already shows {', '.join(matched[:4])}"
                f" which align well with {role}."
            )
        else:
            reason = f"{role} is still possible, but you need to build the core skill set first."
        recs.append(
            {
                "role": role,
                "required_skills": required,
                "matched_skills": matched,
                "missing_skills": missing,
                "match_score": score,
                "reason": reason,
            }
        )
    recs.sort(key=lambda x: x["match_score"], reverse=True)
    return recs


def get_role_by_name(recommendations, selected_role):
    for item in recommendations:
        if item["role"] == selected_role:
            return item
    return recommendations[0] if recommendations else None


def build_skill_gap_data(student_skills, selected_role_match):
    if not selected_role_match:
        return {
            "missing_skills": [],
            "matched_skills": [],
            "learning_guidance": {},
            "reference_links": [],
            "practice_sites": [],
            "daily_plan": [],
        }

    learning = {}
    reference_links = []
    practice_sites = []

    for skill in selected_role_match["missing_skills"]:
        guidance = LEARNING_GUIDANCE.get(skill, default_learning_guidance(skill))
        learning[skill] = guidance
        reference_links.extend(guidance.get("links", []))
        practice_sites.extend(guidance.get("practice_sites", []))

    unique_links = []
    for link in reference_links:
        if link not in unique_links:
            unique_links.append(link)

    unique_sites = []
    for site in practice_sites:
        if site not in unique_sites:
            unique_sites.append(site)

    daily_plan = []
    for day, skill in enumerate(selected_role_match["missing_skills"][:10], start=1):
        guidance = learning[skill]
        topic = guidance.get("topics", ["Core fundamentals"])[0]
        daily_plan.append(
            {
                "day": day,
                "skill": skill,
                "task": f"Complete a focused lesson on {topic} and finish one practice task.",
                "minutes": guidance.get("daily_minutes", 30),
            }
        )

    return {
        "missing_skills": selected_role_match["missing_skills"],
        "matched_skills": selected_role_match["matched_skills"],
        "learning_guidance": learning,
        "reference_links": unique_links[:10],
        "practice_sites": unique_sites[:10],
        "daily_plan": daily_plan,
    }
