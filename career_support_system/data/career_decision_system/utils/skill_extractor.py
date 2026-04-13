SKILLS = [
    "Python",
    "SQL",
    "Machine Learning",
    "Data Analysis",
    "Java",
    "C++",
    "HTML",
    "CSS",
    "JavaScript",
    "Deep Learning",
    "Statistics",
    "TensorFlow",
    "Data Visualization",
    "Programming",
    "Data Structures",
    "Algorithms",
    "Excel",
    "Power BI",
    "React",
    "Git",
    "Responsive Design",
    "APIs",
    "Flask",
]


def get_nlp():
    # Fallback to a blank English model if full model is unavailable.
    try:
        import spacy

        return spacy.load("en_core_web_sm")
    except Exception:
        try:
            import spacy

            return spacy.blank("en")
        except Exception:
            return None


NLP = get_nlp()


def extract_skills(resume_text):
    normalized_text = resume_text.lower()
    if NLP is not None:
        doc = NLP(resume_text.lower())
        normalized_text = " ".join([token.text for token in doc])

    found = []
    for skill in SKILLS:
        if skill.lower() in normalized_text:
            found.append(skill)

    return sorted(list(set(found)))
