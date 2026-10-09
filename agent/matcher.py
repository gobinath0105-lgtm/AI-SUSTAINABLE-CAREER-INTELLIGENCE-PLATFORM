"""
Local Job Relevance Filter

Purpose:
- Remove obviously irrelevant jobs.
- Allow AI/ML/Python-related jobs to reach Gemini.
- Do NOT make the final hiring decision here.
"""

import re


# ============================================================
# SKILLS
# ============================================================

SKILLS = [
    "Python",
    "SQL",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "Keras",
    "PyTorch",
    "Scikit-learn",
    "Pandas",
    "NumPy",
    "NLP",
    "Transformers",
    "LLM",
    "Generative AI",
    "RAG",
    "LangChain",
    "Vector Database",
    "Embeddings",
    "FastAPI",
    "Flask",
    "REST API",
    "Docker",
    "Git",
    "GitHub",
    "OpenCV",
    "YOLO",
    "CNN",
    "RNN",
    "LSTM",
    "Computer Vision",
    "Statistics",
    "Matplotlib",
    "Excel",
    "Power BI",
    "Streamlit",
    "KNN",
    "PCA",
    "XGBoost",
]


# ============================================================
# AI / DATA ROLE KEYWORDS
# ============================================================

AI_ROLE_KEYWORDS = [
    "ai engineer",
    "ai developer",
    "artificial intelligence engineer",
    "artificial intelligence developer",

    "machine learning engineer",
    "machine learning developer",
    "ml engineer",
    "ml developer",

    "deep learning engineer",
    "deep learning developer",

    "nlp engineer",
    "nlp developer",
    "natural language processing",

    "generative ai engineer",
    "generative ai developer",
    "genai engineer",
    "genai developer",

    "llm engineer",
    "llm developer",

    "computer vision engineer",
    "computer vision developer",

    "data scientist",
    "data science",

    "ai/ml engineer",
    "ai/ml intern",
    "ai intern",
    "ai engineer intern",

    "machine learning intern",
    "ml intern",

    "deep learning intern",
    "nlp intern",

    "data science intern",

    "python ai developer",
    "python ai engineer",

    "backend ai engineer",
]


# ============================================================
# AI / DATA DOMAIN KEYWORDS
# ============================================================

AI_DOMAIN_KEYWORDS = [
    "artificial intelligence",
    "machine learning",
    "deep learning",
    "natural language processing",
    "nlp",
    "generative ai",
    "genai",
    "large language model",
    "llm",
    "computer vision",
    "data science",
    "neural network",
    "transformer",
    "transformers",
    "rag",
    "retrieval augmented generation",
    "retrieval-augmented generation",
    "ai model",
    "ai systems",
    "ai tools",
    "ai application",
]


# ============================================================
# AI-RELATED JOB PHRASES
# These help jobs whose title is not exactly "AI Engineer"
# ============================================================

AI_JOB_PHRASES = [
    "ai trainer",
    "ai code trainer",
    "ai coding",
    "ai evaluation",
    "ai evaluator",
    "ai data",
    "ai model",
    "ai assistant",
    "ai research",
    "ai researcher",
    "machine learning",
    "ml model",
    "ml system",
    "llm",
    "generative ai",
    "genai",
    "natural language",
    "computer vision",
    "deep learning",
]


# ============================================================
# IRRELEVANT JOB KEYWORDS
# ============================================================

IRRELEVANT_ROLE_KEYWORDS = [
    "copywriter",
    "copy writer",
    "content writer",
    "content writing",
    "freelance writer",

    "service desk",
    "help desk",
    "technical support",
    "customer support",
    "customer service",

    "react developer",
    "react.js developer",
    "frontend developer",
    "front end developer",
    "frontend engineer",
    "front end engineer",
    "ui developer",
    "ui engineer",

    "graphic designer",
    "video editor",

    "sales",
    "marketing",
    "hr",
    "recruiter",
    "recruitment",

    "accountant",
    "accounting",
]


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    """
    Convert text into a simple lowercase searchable format.
    """

    if not text:
        return ""

    text = str(text).lower()

    # Convert separators into spaces
    text = re.sub(r"[-_/]", " ", text)

    # Remove special characters
    text = re.sub(r"[^a-z0-9+#.\s]", " ", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text):
    """
    Find known skills inside text.
    """

    normalized = normalize_text(text)

    found = []

    for skill in SKILLS:
        skill_normalized = normalize_text(skill)

        if skill_normalized and skill_normalized in normalized:
            found.append(skill)

    return found


# ============================================================
# ROLE CHECK
# ============================================================

def is_ai_role(job_title):
    """
    Check whether the job title strongly belongs to AI/Data.
    """

    title = normalize_text(job_title)

    if not title:
        return False

    # First reject clearly unrelated roles
    for keyword in IRRELEVANT_ROLE_KEYWORDS:
        if normalize_text(keyword) in title:
            return False

    # Strong AI/Data role
    for keyword in AI_ROLE_KEYWORDS:
        if normalize_text(keyword) in title:
            return True

    return False


# ============================================================
# DOMAIN CHECK
# ============================================================

def contains_ai_domain(text):
    """
    Check whether the job description contains AI/Data concepts.
    """

    normalized = normalize_text(text)

    matches = []

    for keyword in AI_DOMAIN_KEYWORDS:
        if normalize_text(keyword) in normalized:
            matches.append(keyword)

    return matches


# ============================================================
# AI JOB PHRASE CHECK
# ============================================================

def contains_ai_job_phrase(text):
    """
    Detect AI-related phrases even when the title
    is not a standard AI job title.
    """

    normalized = normalize_text(text)

    matches = []

    for phrase in AI_JOB_PHRASES:
        if normalize_text(phrase) in normalized:
            matches.append(phrase)

    return matches


# ============================================================
# MAIN RELEVANCE FILTER
# ============================================================

def is_relevant_job(resume_text, job_title, job_description=""):
    """
    Decide whether a job should be sent to Gemini.

    IMPORTANT:
    This is only a pre-filter.
    Gemini makes the final job suitability decision.
    """

    title = normalize_text(job_title)
    description = normalize_text(job_description)
    full_job_text = f"{title} {description}"

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(full_job_text)

    matched_skills = [
        skill for skill in job_skills
        if skill in resume_skills
    ]

    # --------------------------------------------------------
    # 1. Reject obviously unrelated roles
    # --------------------------------------------------------

    for keyword in IRRELEVANT_ROLE_KEYWORDS:

        if normalize_text(keyword) in title:

            return {
                "relevant": False,
                "relevance_score": 0,
                "reason": "Job title is outside the candidate's AI/Data career target.",
                "matched_skills": [],
                "resume_skills": resume_skills,
                "job_skills": job_skills,
                "role_matches": [],
                "domain_matches": [],
            }

    # --------------------------------------------------------
    # 2. Strong AI/Data role title
    # --------------------------------------------------------

    role_matches = [
        keyword
        for keyword in AI_ROLE_KEYWORDS
        if normalize_text(keyword) in title
    ]

    if role_matches:

        score = min(
            100,
            60 + (len(matched_skills) * 10)
        )

        return {
            "relevant": True,
            "relevance_score": score,
            "reason": (
                "AI/Data-related role with matching resume skills: "
                + ", ".join(matched_skills)
            ),
            "matched_skills": matched_skills,
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "role_matches": role_matches,
            "domain_matches": [],
        }

    # --------------------------------------------------------
    # 3. AI-related phrase in title OR description
    # --------------------------------------------------------

    ai_phrase_matches = contains_ai_job_phrase(full_job_text)

    domain_matches = contains_ai_domain(full_job_text)

    if ai_phrase_matches or domain_matches:

        # We don't require many matching skills here.
        # Gemini should make the final decision.

        score = min(
            90,
            50 + (len(matched_skills) * 10)
        )

        return {
            "relevant": True,
            "relevance_score": score,
            "reason": (
                "Job contains AI-related responsibilities or technology. "
                "Sending to Gemini for deeper analysis."
            ),
            "matched_skills": matched_skills,
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "role_matches": ai_phrase_matches,
            "domain_matches": domain_matches,
        }

    # --------------------------------------------------------
    # 4. Python job with AI/Data skills
    # --------------------------------------------------------

    has_python = "python" in title or "python" in description

    ai_skill_count = sum(
        1
        for skill in [
            "Machine Learning",
            "Deep Learning",
            "NLP",
            "LLM",
            "Generative AI",
            "RAG",
            "Transformers",
            "Computer Vision",
        ]
        if normalize_text(skill) in full_job_text
    )

    if has_python and ai_skill_count >= 1:

        score = min(
            85,
            45 + (len(matched_skills) * 10)
        )

        return {
            "relevant": True,
            "relevance_score": score,
            "reason": (
                "Python role with AI/Data-related requirements. "
                "Sending to Gemini for deeper analysis."
            ),
            "matched_skills": matched_skills,
            "resume_skills": resume_skills,
            "job_skills": job_skills,
            "role_matches": [],
            "domain_matches": [],
        }

    # --------------------------------------------------------
    # 5. Not relevant
    # --------------------------------------------------------

    return {
        "relevant": False,
        "relevance_score": 0,
        "reason": "Job does not strongly match the candidate's AI/Data career target.",
        "matched_skills": [],
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "role_matches": [],
        "domain_matches": [],
    }


# ============================================================
# OPTIONAL FINAL SKILL MATCH
# ============================================================

def match_job(resume_text, job_title, job_description=""):
    """
    Simple skill matching.

    This is separate from AI analysis.
    """

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(
        f"{job_title} {job_description}"
    )

    matched_skills = [
        skill
        for skill in job_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill
        for skill in job_skills
        if skill not in resume_skills
    ]

    if job_skills:
        score = round(
            (len(matched_skills) / len(job_skills)) * 100,
            2
        )
    else:
        score = 0

    return {
        "score": score,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "resume_skills": resume_skills,
        "job_skills": job_skills,
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    resume = """
    Gobinath
    AI Engineer Intern Candidate
    B.Tech Artificial Intelligence and Data Science

    Python
    SQL
    Machine Learning
    Deep Learning
    TensorFlow
    Keras
    NLP
    LLM
    Transformers
    RAG
    LangChain
    Embeddings
    Vector Database
    Scikit-learn
    Pandas
    FastAPI
    Git
    """

    test_jobs = [

        {
            "title": "AI Engineer Intern",
            "description": """
            Work on Python, machine learning,
            NLP and TensorFlow projects.
            """
        },

        {
            "title": "Machine Learning Engineer",
            "description": """
            Build machine learning models using
            Python, SQL and TensorFlow.
            """
        },

        {
            "title": "Software Engineer / AI Code Trainer (Python, Web, Full Stack)",
            "description": """
            Evaluate AI-generated code and help improve
            machine learning and AI coding systems.
            Python programming required.
            """
        },

        {
            "title": "Senior React Full-stack Developer",
            "description": """
            Build React applications and full-stack
            software using Python and cloud platforms.
            """
        },

        {
            "title": "Freelance Copywriter",
            "description": """
            Write marketing content and articles.
            """
        },

        {
            "title": "Tier III Service Desk Engineer",
            "description": """
            Provide technical support and troubleshoot
            enterprise systems.
            """
        },
    ]

    print("=" * 70)
    print("IMPROVED LOCAL JOB RELEVANCE FILTER")
    print("=" * 70)

    for job in test_jobs:

        result = is_relevant_job(
            resume,
            job["title"],
            job["description"]
        )

        print()
        print(f"Job: {job['title']}")
        print(f"Relevant: {result['relevant']}")
        print(f"Score: {result['relevance_score']}")
        print(f"Reason: {result['reason']}")

        if result["matched_skills"]:
            print(
                "Matched:",
                ", ".join(result["matched_skills"])
            )

    print()
    print("=" * 70)
    print("TEST COMPLETED")
    print("=" * 70)