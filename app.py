# ============================================================
# AI SUSTAINABLE CAREER INTELLIGENCE PLATFORM
# ============================================================

import streamlit as st
from pypdf import PdfReader
import pandas as pd
import re
from groq import Groq


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Career Intelligence Platform",
    page_icon="🚀",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🚀 AI Sustainable Career Intelligence Platform")

st.write(
    """
    Upload your resume and discover:

    - 🧠 Your skills
    - 💼 Best matching jobs + job-skill intelligence
    - 📊 Skill gaps
    - 🎯 Target-role analysis
    - 📈 Multi-role skill impact simulation
    - 🔥 Skill priority ranking
    - 🛠️ Personalized project recommendations
    - 📊 Career intelligence dashboard
    - 📌 Career progress tracking
    - 🗺️ Career roadmap
    - 🤖 AI career advisor
    """
)


# ============================================================
# SKILL DATABASE
# ============================================================

skills_database = [
    "Python",
    "Java",
    "C++",
    "SQL",
    "Excel",
    "Machine Learning",
    "Deep Learning",
    "AI",
    "TensorFlow",
    "Keras",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Matplotlib",
    "Statistics",
    "NLP",
    "Natural Language Processing",
    "Transformers",
    "LLM",
    "Generative AI",
    "RAG",
    "LangChain",
    "Vector Database",
    "Embeddings",
    "Semantic Search",
    "Git",
    "GitHub",
    "Docker",
    "FastAPI",
    "Flask",
    "REST API",
    "Streamlit",
    "OpenCV",
    "YOLO",
    "CNN",
    "RNN",
    "LSTM",
    "Computer Vision",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "AWS",
    "Azure",
    "Google Cloud",
    "Power BI"
]


# ============================================================
# SKILL ALIASES
# ============================================================

skill_aliases = {
    "ml": "Machine Learning",
    "machine learning": "Machine Learning",

    "dl": "Deep Learning",
    "deep learning": "Deep Learning",

    "tf": "TensorFlow",
    "tensorflow": "TensorFlow",

    "pytorch": "PyTorch",

    "sklearn": "Scikit-learn",
    "scikit learn": "Scikit-learn",
    "scikit-learn": "Scikit-learn",

    "pd": "Pandas",
    "pandas": "Pandas",

    "np": "NumPy",
    "numpy": "NumPy",

    "nlp": "NLP",
    "natural language processing": "Natural Language Processing",

    "transformer": "Transformers",
    "transformers": "Transformers",

    "llm": "LLM",

    "genai": "Generative AI",
    "generative ai": "Generative AI",

    "rag": "RAG",

    "langchain": "LangChain",

    "vector db": "Vector Database",
    "vector database": "Vector Database",
    "vector databases": "Vector Database",

    "embedding": "Embeddings",
    "embeddings": "Embeddings",

    "semantic search": "Semantic Search",

    "git": "Git",
    "github": "GitHub",

    "docker": "Docker",

    "fastapi": "FastAPI",

    "flask": "Flask",

    "rest api": "REST API",

    "opencv": "OpenCV",

    "yolo": "YOLO",

    "cnn": "CNN",

    "rnn": "RNN",

    "lstm": "LSTM",

    "computer vision": "Computer Vision",

    "sql": "SQL",

    "statistics": "Statistics",

    "power bi": "Power BI"
}


# ============================================================
# ROLE LEARNING ORDER
# ============================================================

role_learning_order = {

    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "NLP",
        "Transformers",
        "LLM",
        "Generative AI",
        "Embeddings",
        "RAG",
        "Vector Database",
        "LangChain",
        "FastAPI",
        "Docker",
        "Git"
    ],

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "NumPy",
        "Pandas",
        "Scikit-learn",
        "Statistics",
        "TensorFlow",
        "SQL",
        "Git",
        "Docker"
    ],

    "Data Scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Statistics",
        "Machine Learning",
        "Scikit-learn",
        "Matplotlib"
    ],

    "Deep Learning Engineer": [
        "Python",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "CNN",
        "RNN",
        "LSTM",
        "Computer Vision",
        "Git"
    ],

    "NLP Engineer": [
        "Python",
        "NLP",
        "Natural Language Processing",
        "Transformers",
        "LLM",
        "PyTorch",
        "TensorFlow"
    ],

    "Generative AI Engineer": [
        "Python",
        "LLM",
        "Generative AI",
        "Embeddings",
        "RAG",
        "LangChain",
        "Vector Database",
        "FastAPI",
        "Docker"
    ],

    "Data Analyst": [
        "Python",
        "SQL",
        "Pandas",
        "Excel",
        "Statistics",
        "Matplotlib",
        "Power BI"
    ],

    "Computer Vision Engineer": [
        "Python",
        "OpenCV",
        "YOLO",
        "Deep Learning",
        "TensorFlow",
        "PyTorch",
        "CNN",
        "Computer Vision"
    ],

    "Backend AI Engineer": [
        "Python",
        "FastAPI",
        "Flask",
        "REST API",
        "Docker",
        "Git",
        "SQL",
        "Machine Learning"
    ],

    "AI/ML Intern": [
        "Python",
        "SQL",
        "Machine Learning",
        "Pandas",
        "Scikit-learn",
        "Git"
    ]
}


# ============================================================
# LEARNING INFORMATION
# ============================================================

learning_information = {

    "Python": "Build strong Python programming and OOP skills.",
    "SQL": "Learn databases, SELECT, JOIN, GROUP BY and data querying.",
    "Machine Learning": "Learn supervised and unsupervised machine learning.",
    "Deep Learning": "Learn neural networks, CNNs, RNNs and model training.",
    "NLP": "Learn text processing, classification and language understanding.",
    "Transformers": "Learn attention, transformer architecture and modern NLP.",
    "LLM": "Learn large language model concepts and applications.",
    "Generative AI": "Learn how to build applications using generative models.",
    "RAG": "Learn retrieval augmented generation using external knowledge.",
    "Vector Database": "Learn embeddings, vector search and semantic retrieval.",
    "Embeddings": "Learn how text is converted into numerical representations.",
    "LangChain": "Learn frameworks for building LLM applications.",
    "FastAPI": "Learn how to expose AI models through APIs.",
    "Docker": "Learn containerization and application deployment.",
    "Git": "Learn version control and collaboration.",
    "GitHub": "Build and maintain professional software repositories.",
    "TensorFlow": "Learn deep learning model development using TensorFlow.",
    "PyTorch": "Learn deep learning model development using PyTorch.",
    "Scikit-learn": "Learn practical classical machine learning.",
    "Pandas": "Learn data cleaning and analysis.",
    "NumPy": "Learn numerical computing with Python.",
    "Statistics": "Learn probability, distributions and statistical analysis.",
    "OpenCV": "Learn computer vision image and video processing.",
    "YOLO": "Learn real-time object detection.",
    "Computer Vision": "Learn image understanding and visual AI.",
    "CNN": "Learn convolutional neural networks for images.",
    "RNN": "Learn recurrent neural networks for sequential data.",
    "LSTM": "Learn long-term sequence modelling."
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(text):

    text = str(text).lower()

    text = text.replace("-", " ")
    text = text.replace("_", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def normalize_role_column(role):

    return (
        str(role)
        .strip()
        .lower()
        .replace("/", "_")
        .replace(" ", "_")
        .replace("-", "_")
    )



# ============================================================
# UPGRADED CAREER INTELLIGENCE HELPERS
# ============================================================

def parse_skill_weight_string(value):
    weights = {}
    if pd.isna(value):
        return weights
    text = str(value).strip()
    if not text:
        return weights
    for item in text.split(","):
        item = item.strip()
        if ":" not in item:
            continue
        skill, weight = item.rsplit(":", 1)
        try:
            weights[normalize_text(skill)] = float(weight)
        except ValueError:
            continue
    return weights


def calculate_weighted_job_match(required_skills, detected_skill_set, skill_weights=None):
    skill_weights = skill_weights or {}
    matched = []
    missing = []
    total_weight = 0
    matched_weight = 0

    for skill in required_skills:
        skill_norm = normalize_text(skill)
        weight = float(skill_weights.get(skill_norm, 1))
        if weight <= 0:
            weight = 1
        total_weight += weight

        if skill_norm in detected_skill_set:
            matched.append(skill)
            matched_weight += weight
        else:
            missing.append(skill)

    score = (matched_weight / total_weight) * 100 if total_weight else 0

    return (
        round(score, 1),
        matched,
        missing,
        round(matched_weight, 2),
        round(total_weight, 2)
    )


def calculate_role_match(role, user_skills, impact_df, impact_column):
    role_skills = role_learning_order.get(role, [])
    user_skill_set = {normalize_text(skill) for skill in user_skills}

    matched = []
    missing = []
    weighted_total = 0
    weighted_matched = 0
    impact_lookup = {}

    if impact_df is not None and not impact_df.empty and impact_column in impact_df.columns:
        for _, row in impact_df.iterrows():
            try:
                impact_lookup[normalize_text(row["skill"])] = float(row[impact_column])
            except Exception:
                pass

    for skill in role_skills:
        skill_norm = normalize_text(skill)
        importance = impact_lookup.get(skill_norm, 5)
        weight = 1 + (importance / 10)
        weighted_total += weight

        if skill_norm in user_skill_set:
            matched.append(skill)
            weighted_matched += weight
        else:
            missing.append(skill)

    score = weighted_matched / weighted_total * 100 if weighted_total else 0

    return round(score, 1), matched, missing


def get_role_impact_lookup(impact_df, role):
    lookup = {}

    if impact_df is None or impact_df.empty:
        return lookup

    column = normalize_role_column(role)

    if column not in impact_df.columns:
        return lookup

    for _, row in impact_df.iterrows():
        try:
            lookup[normalize_text(row["skill"])] = float(row[column])
        except Exception:
            pass

    return lookup


def simulate_role_improvement(role, user_skills, selected_skills, impact_df):
    baseline, _, missing = calculate_role_match(
        role,
        user_skills,
        impact_df,
        normalize_role_column(role)
    )

    impact_lookup = get_role_impact_lookup(impact_df, role)

    missing_norms = {normalize_text(m) for m in missing}

    total_possible_impact = sum(
        impact_lookup.get(normalize_text(skill), 0)
        for skill in missing
    )

    selected_impact = sum(
        impact_lookup.get(normalize_text(skill), 0)
        for skill in selected_skills
        if normalize_text(skill) in missing_norms
    )

    maximum_improvement = 100 - baseline
    ratio = selected_impact / total_possible_impact if total_possible_impact else 0
    improvement = maximum_improvement * ratio
    estimated = min(baseline + improvement, 100)

    return (
        round(baseline, 1),
        round(estimated, 1),
        round(improvement, 1),
        round(selected_impact, 1),
        missing
    )


def safe_csv_download(df, filename):
    return df.to_csv(index=False).encode("utf-8")


# ============================================================
# ATS SCORE + RESUME IMPROVEMENT HELPERS
# ============================================================

def calculate_ats_score(
    resume_text,
    target_role,
    detected_skills,
    role_required_skills,
    job_required_skills=None
):
    """
    Calculates an ATS-style resume score.

    This is an internal scoring system for the platform.
    It is NOT an official ATS score from any company.
    """

    resume_text_lower = normalize_text(resume_text)

    # --------------------------------------------------------
    # 1. Skill Coverage Score - 40 points
    # --------------------------------------------------------
    role_required_skills = [
        skill for skill in role_required_skills
        if skill
    ]

    detected_normalized = {
        normalize_text(skill)
        for skill in detected_skills
    }

    matched_role_skills = []

    for skill in role_required_skills:
        if normalize_text(skill) in detected_normalized:
            matched_role_skills.append(skill)

    if role_required_skills:
        skill_coverage = (
            len(matched_role_skills)
            / len(role_required_skills)
        ) * 100
    else:
        skill_coverage = 0

    skill_score = skill_coverage * 0.40

    # --------------------------------------------------------
    # 2. Keyword Coverage - 25 points
    # --------------------------------------------------------
    keywords = set()

    for skill in role_required_skills:
        keywords.add(normalize_text(skill))

    if job_required_skills:
        for skill in job_required_skills:
            keywords.add(normalize_text(skill))

    matched_keywords = [
        keyword
        for keyword in keywords
        if keyword and keyword in resume_text_lower
    ]

    if keywords:
        keyword_coverage = (
            len(matched_keywords)
            / len(keywords)
        ) * 100
    else:
        keyword_coverage = 0

    keyword_score = keyword_coverage * 0.25

    # --------------------------------------------------------
    # 3. Resume Length / Content Score - 15 points
    # --------------------------------------------------------
    word_count = len(resume_text.split())

    if 400 <= word_count <= 1200:
        content_score = 100
    elif 250 <= word_count < 400:
        content_score = 75
    elif 1200 < word_count <= 1600:
        content_score = 80
    elif word_count > 1600:
        content_score = 60
    else:
        content_score = 40

    content_points = content_score * 0.15

    # --------------------------------------------------------
    # 4. Section Completeness - 20 points
    # --------------------------------------------------------
    section_keywords = {
        "experience": [
            "experience",
            "work experience",
            "employment"
        ],
        "education": [
            "education",
            "academic",
            "degree"
        ],
        "projects": [
            "projects",
            "project"
        ],
        "skills": [
            "skills",
            "technical skills"
        ],
        "contact": [
            "email",
            "phone",
            "linkedin",
            "github"
        ]
    }

    section_results = {}

    for section, keywords_list in section_keywords.items():
        section_results[section] = any(
            keyword in resume_text_lower
            for keyword in keywords_list
        )

    sections_found = sum(section_results.values())

    section_score = (
        sections_found / len(section_keywords)
    ) * 100

    section_points = section_score * 0.20

    # --------------------------------------------------------
    # Final ATS-style score
    # --------------------------------------------------------
    final_score = (
        skill_score
        + keyword_score
        + content_points
        + section_points
    )

    final_score = round(
        min(max(final_score, 0), 100),
        1
    )

    return {
        "ats_score": final_score,
        "skill_coverage": round(skill_coverage, 1),
        "keyword_coverage": round(keyword_coverage, 1),
        "word_count": word_count,
        "sections_found": sections_found,
        "total_sections": len(section_keywords),
        "matched_role_skills": matched_role_skills,
        "missing_role_skills": [
            skill
            for skill in role_required_skills
            if skill not in matched_role_skills
        ],
        "section_results": section_results,
        "matched_keywords": matched_keywords
    }


def generate_resume_improvement_tips(
    ats_result,
    target_role
):
    """
    Generates rule-based resume improvement recommendations.
    """

    tips = []

    score = ats_result["ats_score"]
    word_count = ats_result["word_count"]

    missing_skills = ats_result["missing_role_skills"]

    section_results = ats_result["section_results"]

    # --------------------------------------------------------
    # ATS score
    # --------------------------------------------------------
    if score < 60:
        tips.append(
            "Your resume needs stronger alignment with the target role."
        )
    elif score < 80:
        tips.append(
            "Your resume has a reasonable foundation, but it can be better aligned with the target role."
        )
    else:
        tips.append(
            "Your resume has strong alignment with the selected target role."
        )

    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------
    if missing_skills:
        important_missing = missing_skills[:5]

        tips.append(
            "Consider adding relevant evidence for: "
            + ", ".join(important_missing)
            + "."
        )

    # --------------------------------------------------------
    # Resume sections
    # --------------------------------------------------------
    if not section_results.get("projects", False):
        tips.append(
            "Add a Projects section with 2–4 relevant technical projects."
        )

    if not section_results.get("skills", False):
        tips.append(
            "Add a clearly labelled Technical Skills section."
        )

    if not section_results.get("education", False):
        tips.append(
            "Add a clearly labelled Education section."
        )

    if not section_results.get("experience", False):
        tips.append(
            "Add Experience or Internship information if applicable."
        )

    if not section_results.get("contact", False):
        tips.append(
            "Make sure your email, phone, LinkedIn, or GitHub information is clearly visible."
        )

    # --------------------------------------------------------
    # Resume length
    # --------------------------------------------------------
    if word_count < 250:
        tips.append(
            "Your resume appears short. Add relevant project, education, or experience details."
        )
    elif word_count > 1600:
        tips.append(
            "Your resume may be too long. Remove repetitive or low-value information."
        )

    # --------------------------------------------------------
    # Generic improvement
    # --------------------------------------------------------
    tips.append(
        "Use keywords naturally in project and experience descriptions instead of only listing them in the skills section."
    )

    tips.append(
        "Add measurable results to projects when possible, such as accuracy, dataset size, latency, or improvement percentage."
    )

    return tips


# ============================================================
# STEP 1 — UPLOAD RESUME
# ============================================================

st.header("📄 Step 1 — Upload Resume")


uploaded_file = st.file_uploader(
    "Upload your resume PDF",
    type=["pdf"]
)


if uploaded_file is None:

    st.info(
        "👆 Upload a PDF resume to start."
    )

    st.stop()


# ============================================================
# EXTRACT PDF TEXT
# ============================================================

try:

    reader = PdfReader(
        uploaded_file
    )

    resume_text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            resume_text += " " + page_text

except Exception as e:

    st.error(
        f"Could not read PDF: {e}"
    )

    st.stop()


resume_text = re.sub(
    r"(?<=\w)\s(?=\w)",
    "",
    resume_text
)

resume_text = re.sub(
    r"\s+",
    " ",
    resume_text
).strip()


if not resume_text:

    st.error(
        "No readable text was found."
    )

    st.stop()


with st.expander(
    "🔎 View extracted resume text"
):

    st.write(
        resume_text
    )


# ============================================================
# STEP 2 — SKILL EXTRACTION
# ============================================================

st.header(
    "🧠 Step 2 — Resume Skill Intelligence"
)


resume_lower = normalize_text(
    resume_text
)


detected_skills = []


for skill in skills_database:

    skill_normalized = normalize_text(
        skill
    )

    if skill_normalized in resume_lower:

        detected_skills.append(
            skill
        )


for alias, standard_skill in skill_aliases.items():

    alias_normalized = normalize_text(
        alias
    )

    if alias_normalized in resume_lower:

        if standard_skill not in detected_skills:

            detected_skills.append(
                standard_skill
            )


detected_skills = list(
    dict.fromkeys(
        detected_skills
    )
)


if detected_skills:

    st.success(
        f"Detected {len(detected_skills)} skills."
    )

    skill_columns = st.columns(4)

    for index, skill in enumerate(
        detected_skills
    ):

        with skill_columns[
            index % 4
        ]:

            st.markdown(
                f"✅ **{skill}**"
            )

else:

    st.warning(
        "No skills detected."
    )


# ============================================================
# STEP 3 — JOB MATCHING + JOB-SKILL INTELLIGENCE
# ============================================================

st.header("💼 Step 3 — Intelligent Job Matching")

try:
    jobs = pd.read_csv("jobs.csv")
except Exception as e:
    st.error(f"Could not load jobs.csv: {e}")
    st.stop()

required_columns = ["job_id", "job_title", "company", "required_skills"]

for column in required_columns:
    if column not in jobs.columns:
        st.error(f"Missing column '{column}' in jobs.csv")
        st.stop()

detected_skill_set = {normalize_text(skill) for skill in detected_skills}

job_results = []

for _, job in jobs.iterrows():
    required_skills = [
        skill.strip()
        for skill in str(job["required_skills"]).split(",")
        if skill.strip()
    ]

    skill_weights = (
        parse_skill_weight_string(job["skill_weights"])
        if "skill_weights" in jobs.columns
        else {}
    )

    weighted_match, matched_skills, missing_skills, matched_weight, total_weight = (
        calculate_weighted_job_match(
            required_skills,
            detected_skill_set,
            skill_weights
        )
    )

    job_results.append({
        "Job Title": job["job_title"],
        "Company": job["company"],
        "Match %": weighted_match,
        "Matched Skills": ", ".join(matched_skills),
        "Missing Skills": ", ".join(missing_skills),
        "Matched Weight": matched_weight,
        "Total Skill Weight": total_weight
    })

job_results_df = pd.DataFrame(job_results).sort_values(
    "Match %",
    ascending=False
).reset_index(drop=True)

st.subheader("🏆 Best Matching Jobs")

st.dataframe(
    job_results_df[
        ["Job Title", "Company", "Match %", "Matched Skills", "Missing Skills"]
    ],
    use_container_width=True,
    hide_index=True
)

st.info(
    "💡 Job matching supports skill importance. If jobs.csv contains "
    "a skill_weights column such as Python:5,Machine Learning:5,SQL:3, "
    "critical skills receive more importance. Without it, all skills "
    "receive equal weight."
)

st.subheader("🔍 Job-Skill Intelligence")

if not job_results_df.empty:
    selected_job_name = st.selectbox(
        "Inspect a job",
        job_results_df["Job Title"].tolist(),
        key="job_intelligence_selector"
    )

    selected_job = job_results_df[
        job_results_df["Job Title"] == selected_job_name
    ].iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Weighted Match", f"{selected_job['Match %']}%")
    with c2:
        st.metric("Matched Weight", selected_job["Matched Weight"])
    with c3:
        st.metric("Required Skill Weight", selected_job["Total Skill Weight"])

    missing_text = str(selected_job["Missing Skills"]).strip()

    if missing_text:
        st.warning(f"🎯 Improvement area: {missing_text}")
    else:
        st.success("🎉 Your current skills cover all required skills for this job.")


# ============================================================
# STEP 4 — TARGET ROLE
# ============================================================

st.header(
    "🎯 Step 4 — Target Career Analysis"
)


target_role = st.selectbox(
    "Choose your target career role",
    list(
        role_learning_order.keys()
    )
)


target_skills = role_learning_order[
    target_role
]


detected_skill_normalized = set(
    normalize_text(skill)
    for skill in detected_skills
)


target_matched_skills = []


target_missing_skills = []


for skill in target_skills:

    if (
        normalize_text(skill)
        in detected_skill_normalized
    ):

        target_matched_skills.append(
            skill
        )

    else:

        target_missing_skills.append(
            skill
        )


if target_skills:

    current_match = (
        len(target_matched_skills)
        /
        len(target_skills)
    ) * 100

else:

    current_match = 0


current_match = round(
    current_match,
    1
)


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Current Role Match",
        f"{current_match}%"
    )


with col2:

    st.metric(
        "Skills You Have",
        len(target_matched_skills)
    )


with col3:

    st.metric(
        "Skill Gaps",
        len(target_missing_skills)
    )


st.subheader(
    "💪 Your Strengths"
)


for skill in target_matched_skills:

    st.write(
        f"✅ {skill}"
    )


st.subheader(
    "📚 Your Skill Gaps"
)


for skill in target_missing_skills:

    st.write(
        f"❌ {skill}"
    )


# ============================================================
# STEP 5 — CAREER WHAT-IF SIMULATOR
# ============================================================

st.header("📈 Step 5 — Career What-If Simulator")

try:
    skill_impact = pd.read_csv("skill_impact.csv")
except Exception as e:
    st.error(f"Could not load skill_impact.csv: {e}")
    st.stop()

skill_impact.columns = (
    skill_impact.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("/", "_")
)

skill_impact["skill"] = skill_impact["skill"].astype(str).str.strip().str.lower()

impact_column = normalize_role_column(target_role)

if impact_column not in skill_impact.columns:
    st.error(f"Column '{impact_column}' was not found in skill_impact.csv.")
    st.write(list(skill_impact.columns))
    st.stop()

impact_lookup = {}

for _, row in skill_impact.iterrows():
    try:
        impact_lookup[row["skill"]] = float(row[impact_column])
    except Exception:
        pass


# ============================================================
# 5.1 — ROLE-AWARE JOB INTELLIGENCE
# ============================================================

st.subheader("🎯 5.1 — Target-Role-Aware Job Intelligence")

role_aware_jobs = []

for _, job in jobs.iterrows():
    required_skills = [
        skill.strip()
        for skill in str(job["required_skills"]).split(",")
        if skill.strip()
    ]

    matched = [
        skill for skill in required_skills
        if normalize_text(skill) in detected_skill_set
    ]

    missing = [
        skill for skill in required_skills
        if normalize_text(skill) not in detected_skill_set
    ]

    role_impact = get_role_impact_lookup(skill_impact, target_role)

    total_weight = 0
    matched_weight = 0

    for skill in required_skills:
        importance = role_impact.get(normalize_text(skill), 5)
        weight = 1 + (importance / 10)
        total_weight += weight

        if normalize_text(skill) in detected_skill_set:
            matched_weight += weight

    role_aware_match = (
        matched_weight / total_weight * 100
        if total_weight else 0
    )

    role_aware_jobs.append({
        "Job Title": job["job_title"],
        "Company": job["company"],
        "Career-Aware Match %": round(role_aware_match, 1),
        "Matched Skills": ", ".join(matched),
        "Missing Skills": ", ".join(missing)
    })

role_aware_jobs_df = pd.DataFrame(role_aware_jobs).sort_values(
    "Career-Aware Match %",
    ascending=False
).reset_index(drop=True)

st.dataframe(
    role_aware_jobs_df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Career-aware matching gives greater importance to skills that "
    "are more valuable for your selected target role."
)


# ============================================================
# 5.2 — SINGLE-ROLE WHAT-IF
# ============================================================

st.subheader("🔮 5.2 — What If You Learn These Skills?")

selected_skills = []

for skill in target_missing_skills:
    if st.checkbox(skill, key=f"simulation_{skill}"):
        selected_skills.append(skill)


# ============================================================
# 5.3 — SINGLE-ROLE IMPACT
# ============================================================

if selected_skills:
    st.subheader("📊 5.3 — Skill Impact Calculation")

    skill_scores = {}

    for skill in selected_skills:
        skill_key = skill.strip().lower()

        if skill_key in impact_lookup:
            skill_scores[skill] = impact_lookup[skill_key]

    total_possible_impact = sum(
        impact_lookup.get(skill.strip().lower(), 0)
        for skill in target_missing_skills
    )

    selected_impact = sum(skill_scores.values())
    maximum_improvement = 100 - current_match

    impact_ratio = (
        selected_impact / total_possible_impact
        if total_possible_impact > 0
        else 0
    )

    estimated_improvement = maximum_improvement * impact_ratio
    estimated_match = min(
        current_match + estimated_improvement,
        100
    )

    estimated_match = round(estimated_match, 1)
    estimated_improvement = round(estimated_improvement, 1)

    result_col1, result_col2, result_col3 = st.columns(3)

    with result_col1:
        st.metric("Current Match", f"{current_match}%")
    with result_col2:
        st.metric(
            "Estimated Match",
            f"{estimated_match}%",
            delta=f"+{estimated_improvement}%"
        )
    with result_col3:
        st.metric("Skill Impact", f"{selected_impact:.1f}")

    st.progress(min(int(estimated_match), 100))

    st.caption(
        "This is a skill-coverage simulation, not a hiring probability."
    )

    st.subheader("🔥 5.4 — Skill Priority Ranking")

    priority_data = [
        {"Skill": skill, "Impact Score": score}
        for skill, score in skill_scores.items()
    ]

    priority_df = pd.DataFrame(priority_data).sort_values(
        "Impact Score",
        ascending=False
    ).reset_index(drop=True)

    priority_df.insert(
        0,
        "Priority",
        range(1, len(priority_df) + 1)
    )

    st.dataframe(
        priority_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("🎯 5.5 — Best Next Skill")

    best_skill = priority_df.iloc[0]["Skill"]

    st.success(f"🔥 Best next skill: **{best_skill}**")


# ============================================================
# 5.6 — MULTI-ROLE WHAT-IF SIMULATOR
# ============================================================

st.subheader("🚀 5.6 — Multi-Role Career What-If Simulator")

st.write(
    "Compare how the same learning investment could improve "
    "your readiness across different AI careers."
)

available_roles = list(role_learning_order.keys())

default_roles = (
    [target_role, "Generative AI Engineer"]
    if target_role != "Generative AI Engineer"
    else ["Generative AI Engineer", "AI Engineer"]
)

selected_roles = st.multiselect(
    "Choose careers to compare",
    available_roles,
    default=default_roles,
    key="multi_role_selector"
)

if selected_roles:
    union_missing_skills = []

    detected_norms = {
        normalize_text(skill)
        for skill in detected_skills
    }

    for role in selected_roles:
        for skill in role_learning_order.get(role, []):
            if (
                normalize_text(skill) not in detected_norms
                and skill not in union_missing_skills
            ):
                union_missing_skills.append(skill)

    selected_multi_skills = []

    for skill in union_missing_skills:
        if st.checkbox(
            skill,
            key=f"multi_role_skill_{skill}"
        ):
            selected_multi_skills.append(skill)

    comparison_rows = []

    for role in selected_roles:
        baseline, estimated, improvement, selected_impact, role_missing = (
            simulate_role_improvement(
                role,
                detected_skills,
                selected_multi_skills,
                skill_impact
            )
        )

        comparison_rows.append({
            "Career": role,
            "Current Match %": baseline,
            "Estimated Match %": estimated,
            "Improvement %": improvement,
            "Selected Skill Impact": selected_impact,
            "Remaining Gaps": len(role_missing)
        })

    comparison_df = pd.DataFrame(comparison_rows)

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True
    )

    if selected_multi_skills:
        best_role_after_learning = (
            comparison_df
            .sort_values("Estimated Match %", ascending=False)
            .iloc[0]
        )

        st.success(
            f"🏆 After the selected learning plan, "
            f"**{best_role_after_learning['Career']}** has the "
            f"highest estimated skill coverage at "
            f"**{best_role_after_learning['Estimated Match %']}%**."
        )

        st.caption(
            "This comparison measures structured skill coverage. "
            "It does not predict hiring or employment."
        )
else:
    st.info("Select at least two career roles to compare your career options.")


# ============================================================
# STEP 6 — PROJECT RECOMMENDATION ENGINE
# ============================================================

st.header(
    "🛠️ Step 6 — Personalized Project Recommendation Engine"
)


try:

    projects = pd.read_csv(
        "projects.csv"
    )

except Exception as e:

    st.error(
        f"""
        Could not load projects.csv.

        Make sure projects.csv is in the same
        folder as app.py.

        Error:
        {e}
        """
    )

    st.stop()


required_project_columns = [
    "project_id",
    "project_name",
    "project_description",
    "required_skills",
    "difficulty",
    "portfolio_value"
]


for column in required_project_columns:

    if column not in projects.columns:

        st.error(
            f"Missing column '{column}' "
            f"in projects.csv"
        )

        st.stop()


# ============================================================
# PROJECT MATCHING
# ============================================================

project_results = []


for _, project in projects.iterrows():

    project_skills = [
        skill.strip()
        for skill in str(
            project["required_skills"]
        ).split(",")
    ]


    matching_skills = []


    for project_skill in project_skills:

        if (
            normalize_text(project_skill)
            in detected_skill_normalized
        ):

            matching_skills.append(
                project_skill
            )


    gap_skills = []


    for project_skill in project_skills:

        if (
            normalize_text(project_skill)
            not in detected_skill_normalized
        ):

            gap_skills.append(
                project_skill
            )


    # Skills that this project can help develop
    gap_coverage = []


    for project_skill in gap_skills:

        if (
            normalize_text(project_skill)
            in [
                normalize_text(skill)
                for skill in target_missing_skills
            ]
        ):

            gap_coverage.append(
                project_skill
            )


    if project_skills:

        overall_coverage = (
            len(matching_skills)
            /
            len(project_skills)
        ) * 100

    else:

        overall_coverage = 0


    if target_missing_skills:

        gap_coverage_percentage = (
            len(gap_coverage)
            /
            len(target_missing_skills)
        ) * 100

    else:

        gap_coverage_percentage = 0


    # --------------------------------------------------------
    # PROJECT SCORE
    # --------------------------------------------------------
    #
    # 70% = target skill-gap coverage
    # 30% = existing skill compatibility
    #

    project_score = (
        gap_coverage_percentage * 0.70
        +
        overall_coverage * 0.30
    )


    project_results.append(
        {
            "Project": project[
                "project_name"
            ],

            "Project Score": round(
                project_score,
                1
            ),

            "Gap Skills Covered": ", ".join(
                gap_coverage
            ),

            "Skills You Already Have": ", ".join(
                matching_skills
            ),

            "Difficulty": project[
                "difficulty"
            ],

            "Portfolio Value": project[
                "portfolio_value"
            ],

            "Description": project[
                "project_description"
            ]
        }
    )


project_results_df = pd.DataFrame(
    project_results
)


project_results_df = project_results_df.sort_values(
    "Project Score",
    ascending=False
).reset_index(
    drop=True
)


# ============================================================
# BEST PROJECT
# ============================================================

if not project_results_df.empty:

    best_project = project_results_df.iloc[0]


    st.subheader(
        "🏆 Best Project For You"
    )


    st.success(
        f"""
        ### 🚀 {best_project["Project"]}

        **Project Score:** {best_project["Project Score"]}%

        **Difficulty:** {best_project["Difficulty"]}

        **Portfolio Value:** {best_project["Portfolio Value"]}
        """
    )


    st.write(
        best_project["Description"]
    )


    if best_project[
        "Gap Skills Covered"
    ]:

        st.write(
            "### 🎯 Skills This Project Can Improve"
        )

        for skill in str(
            best_project[
                "Gap Skills Covered"
            ]
        ).split(","):

            if skill.strip():

                st.write(
                    f"✅ {skill.strip()}"
                )


# ============================================================
# PROJECT RANKING
# ============================================================

st.subheader(
    "📊 Recommended Projects Ranking"
)


display_project_df = project_results_df[
    [
        "Project",
        "Project Score",
        "Gap Skills Covered",
        "Difficulty",
        "Portfolio Value"
    ]
]


st.dataframe(
    display_project_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# PROJECT FILTER
# ============================================================

st.subheader(
    "🔎 Explore Projects"
)


selected_difficulty = st.selectbox(
    "Filter by difficulty",
    [
        "All",
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


if selected_difficulty == "All":

    filtered_projects = projects

else:

    filtered_projects = projects[
        projects["difficulty"]
        ==
        selected_difficulty
    ]


for _, project in filtered_projects.iterrows():

    with st.expander(
        f"🛠️ {project['project_name']}"
    ):

        st.write(
            project[
                "project_description"
            ]
        )

        st.write(
            f"**Difficulty:** "
            f"{project['difficulty']}"
        )

        st.write(
            f"**Portfolio Value:** "
            f"{project['portfolio_value']}"
        )

        st.write(
            f"**Required Skills:** "
            f"{project['required_skills']}"
        )


# ============================================================
# STEP 7 — CAREER INTELLIGENCE DASHBOARD
# ============================================================

st.header("📊 Step 7 — Career Intelligence Dashboard")

st.write(
    "A single view of your current career readiness, job opportunities, "
    "skill gaps and portfolio direction."
)

best_job = job_results_df.iloc[0] if not job_results_df.empty else None
best_project_dashboard = (
    project_results_df.iloc[0]
    if not project_results_df.empty
    else None
)
best_role_job = (
    role_aware_jobs_df.iloc[0]
    if not role_aware_jobs_df.empty
    else None
)

dashboard_col1, dashboard_col2, dashboard_col3, dashboard_col4 = st.columns(4)

with dashboard_col1:
    st.metric("Career Match", f"{current_match}%")

with dashboard_col2:
    st.metric("Target Skill Gaps", len(target_missing_skills))

with dashboard_col3:
    st.metric(
        "Best Job Match",
        f"{best_job['Match %']}%" if best_job is not None else "N/A"
    )

with dashboard_col4:
    st.metric(
        "Best Project Score",
        f"{best_project_dashboard['Project Score']}%"
        if best_project_dashboard is not None
        else "N/A"
    )

st.subheader("📈 Career Readiness Snapshot")

dashboard_data = pd.DataFrame({
    "Metric": [
        "Current Role Match",
        "Best Job Match",
        "Best Project Score"
    ],
    "Score": [
        float(current_match),
        float(best_job["Match %"]) if best_job is not None else 0,
        float(best_project_dashboard["Project Score"])
        if best_project_dashboard is not None
        else 0
    ]
})

st.bar_chart(dashboard_data.set_index("Metric"))

dashboard_left, dashboard_right = st.columns(2)

with dashboard_left:
    st.subheader("💪 Current Strengths")

    if target_matched_skills:
        for skill in target_matched_skills:
            st.write(f"✅ {skill}")
    else:
        st.info("No target-role skills detected yet.")

with dashboard_right:
    st.subheader("🎯 Highest-Value Gaps")

    target_impact_lookup = get_role_impact_lookup(
        skill_impact,
        target_role
    )

    gap_dashboard = [
        {
            "Skill": skill,
            "Role Impact": target_impact_lookup.get(
                normalize_text(skill),
                0
            )
        }
        for skill in target_missing_skills
    ]

    if gap_dashboard:
        gap_dashboard_df = pd.DataFrame(gap_dashboard).sort_values(
            "Role Impact",
            ascending=False
        )

        st.dataframe(
            gap_dashboard_df,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("🎉 No skill gaps for this target role.")

st.subheader("🧭 Recommended Direction")

if best_role_job is not None:
    st.info(
        f"Based on your current skills and the importance of skills for "
        f"**{target_role}**, your strongest current job alignment is "
        f"**{best_role_job['Job Title']} at {best_role_job['Company']}** "
        f"with a career-aware score of "
        f"**{best_role_job['Career-Aware Match %']}%**."
    )

if best_project_dashboard is not None:
    st.success(
        f"Build **{best_project_dashboard['Project']}** next. "
        f"It currently has the highest project score for your skill gaps "
        f"and existing skills."
    )


# ============================================================
# STEP 8 — CAREER ROADMAP
# ============================================================


# ============================================================
# STEP 9 — PERSONAL PROGRESS TRACKING
# ============================================================

st.header("📌 Step 9 — Career Progress Tracking")

st.write(
    "Track the skills you have completed and the projects you have "
    "finished. This progress is kept during the current app session."
)

if "completed_skills" not in st.session_state:
    st.session_state.completed_skills = set()

if "completed_projects" not in st.session_state:
    st.session_state.completed_projects = set()

st.subheader("📚 Skill Progress")

detected_norms = {
    normalize_text(skill)
    for skill in detected_skills
}

skill_progress_columns = st.columns(2)

for index, skill in enumerate(target_skills):
    with skill_progress_columns[index % 2]:

        if normalize_text(skill) in detected_norms:
            st.checkbox(
                f"✅ {skill} — Already detected",
                value=True,
                disabled=True,
                key=f"progress_existing_{skill}"
            )
        else:
            completed = st.checkbox(
                f"📖 {skill}",
                value=skill in st.session_state.completed_skills,
                key=f"progress_skill_{skill}"
            )

            if completed:
                st.session_state.completed_skills.add(skill)
            else:
                st.session_state.completed_skills.discard(skill)

completed_target_skills = []

for skill in target_skills:
    detected = normalize_text(skill) in detected_norms
    manually_completed = skill in st.session_state.completed_skills

    if detected or manually_completed:
        completed_target_skills.append(skill)

skill_progress_percent = (
    len(completed_target_skills) / len(target_skills) * 100
    if target_skills
    else 0
)

st.subheader("📊 Skill Completion")

progress_col1, progress_col2, progress_col3 = st.columns(3)

with progress_col1:
    st.metric("Completed Skills", len(completed_target_skills))

with progress_col2:
    st.metric(
        "Remaining Skills",
        max(len(target_skills) - len(completed_target_skills), 0)
    )

with progress_col3:
    st.metric(
        "Learning Progress",
        f"{skill_progress_percent:.1f}%"
    )

st.progress(min(int(skill_progress_percent), 100))


st.subheader("🛠️ Project Progress")

project_names = projects["project_name"].astype(str).tolist()

for project_name in project_names:
    completed = st.checkbox(
        f"🚀 {project_name}",
        value=project_name in st.session_state.completed_projects,
        key=f"progress_project_{project_name}"
    )

    if completed:
        st.session_state.completed_projects.add(project_name)
    else:
        st.session_state.completed_projects.discard(project_name)

completed_project_count = len(st.session_state.completed_projects)

project_progress_percent = (
    completed_project_count / len(project_names) * 100
    if project_names
    else 0
)

st.metric(
    "Projects Completed",
    f"{completed_project_count} / {len(project_names)}"
)

st.progress(min(int(project_progress_percent), 100))


st.subheader("🏆 Overall Career Progress")

overall_progress = (
    skill_progress_percent * 0.7
    + project_progress_percent * 0.3
)

st.metric(
    "Overall Progress",
    f"{overall_progress:.1f}%"
)

st.progress(min(int(overall_progress), 100))

if overall_progress >= 80:
    st.success(
        "🔥 Excellent progress. Focus on projects, deployment and interview preparation."
    )
elif overall_progress >= 50:
    st.info(
        "💪 Good progress. Continue closing your highest-impact skill gaps."
    )
else:
    st.warning(
        "🚀 Keep building. Focus on the recommended skills and your highest-ranked project."
    )

progress_export = pd.DataFrame({
    "Target Role": [target_role],
    "Career Match %": [current_match],
    "Completed Skills": [", ".join(completed_target_skills)],
    "Learning Progress %": [round(skill_progress_percent, 1)],
    "Completed Projects": [
        ", ".join(sorted(st.session_state.completed_projects))
    ],
    "Project Progress %": [round(project_progress_percent, 1)],
    "Overall Progress %": [round(overall_progress, 1)]
})

st.download_button(
    "⬇️ Download My Career Progress",
    data=safe_csv_download(progress_export, "career_progress.csv"),
    file_name="career_progress.csv",
    mime="text/csv"
)


# ============================================================
# STEP 10 — AI CAREER ADVISOR
# ============================================================
# ============================================================
# STEP 10 — AI CAREER ADVISOR
# ============================================================

st.header(
    "🤖 Step 10 — AI Career Advisor"
)


try:

    client = Groq(
        api_key=st.secrets[
            "GROQ_API_KEY"
        ]
    )

except Exception:

    client = None


if st.button(
    "🤖 Generate My AI Career Roadmap"
):

    if client is None:

        st.error(
            """
            Groq API configuration was not found.

            Check:

            .streamlit/secrets.toml
            """
        )

    else:

        strengths_text = ", ".join(
            target_matched_skills
        )

        gaps_text = ", ".join(
            target_missing_skills
        )


        if not project_results_df.empty:

            recommended_projects = "\n".join(
                project_results_df.head(5)[
                    "Project"
                ].tolist()
            )

        else:

            recommended_projects = "None"


        prompt = f"""
You are an AI career advisor.

Candidate target role:
{target_role}

Current role skill match:
{current_match}%

Current strengths:
{strengths_text}

Skill gaps:
{gaps_text}

Recommended projects from the structured
project recommendation engine:
{recommended_projects}

Create a practical career roadmap.

Include:

1. Current position
2. Strengths
3. Skill gaps
4. Learning order
5. Recommended projects
6. GitHub portfolio strategy
7. 30-day plan
8. 60-day plan
9. 90-day plan
10. Interview preparation
11. Resume improvement
12. Job application strategy
13. Progress metrics

Do not claim that learning a skill guarantees employment.

Use the structured analysis as the foundation.
"""


        try:

            with st.spinner(
                "🤖 Generating roadmap..."
            ):

                response = client.chat.completions.create(

                    model="openai/gpt-oss-120b",

                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a practical "
                                "AI career advisor."
                            )
                        },

                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=0.3,

                    max_tokens=4000
                )


            ai_response = (
                response
                .choices[0]
                .message
                .content
            )


            st.subheader(
                "🎯 Personalized AI Career Roadmap"
            )


            st.markdown(
                ai_response
            )


        except Exception as e:

            st.error(
                f"AI roadmap generation failed: {e}"
            )


# ============================================================
# STEP 11 — ATS SCORE + RESUME IMPROVEMENT
# ============================================================

st.header("📝 Step 11 — ATS Score & Resume Improvement")

st.info(
    "This is an ATS-style score created by our Career Intelligence Engine. "
    "It is not an official score from a specific ATS provider."
)

target_role_skills = role_learning_order.get(target_role, [])
job_required_skills_for_ats = []

if not jobs.empty and "required_skills" in jobs.columns:
    target_jobs = jobs[
        jobs["job_title"].astype(str).str.lower().str.contains(
            str(target_role).lower(), na=False
        )
    ]
    if not target_jobs.empty:
        first_job = target_jobs.iloc[0]
        job_required_skills_for_ats = [
            skill.strip() for skill in str(first_job["required_skills"]).split(",")
            if skill.strip()
        ]

ats_result = calculate_ats_score(
    resume_text=resume_text,
    target_role=target_role,
    detected_skills=detected_skills,
    role_required_skills=target_role_skills,
    job_required_skills=job_required_skills_for_ats
)

ats_score = ats_result["ats_score"]

ats_col1, ats_col2, ats_col3 = st.columns(3)
with ats_col1:
    st.metric("ATS-Style Score", f"{ats_score}/100")
with ats_col2:
    st.metric("Skill Coverage", f"{ats_result['skill_coverage']}%")
with ats_col3:
    st.metric("Keyword Coverage", f"{ats_result['keyword_coverage']}%")

st.progress(min(int(ats_score), 100))

if ats_score >= 80:
    st.success("Strong ATS alignment. Your resume is well aligned with the target role.")
elif ats_score >= 60:
    st.warning("Moderate ATS alignment. Your resume has a good foundation but needs improvement.")
else:
    st.error("Low ATS alignment. Your resume needs stronger role-specific keywords and evidence.")

st.subheader("🔎 Missing Role Keywords")
if ats_result["missing_role_skills"]:
    for skill in ats_result["missing_role_skills"]:
        st.markdown(f"- ❌ **{skill}**")
else:
    st.success("No major target-role skill gaps were detected.")

st.subheader("📄 Resume Section Check")
section_names = {
    "experience": "Experience", "education": "Education",
    "projects": "Projects", "skills": "Skills",
    "contact": "Contact Information"
}
for key, display_name in section_names.items():
    st.write(f"{'✅' if ats_result['section_results'].get(key, False) else '❌'} {display_name}")

st.subheader("💡 Resume Improvement Tips")
improvement_tips = generate_resume_improvement_tips(ats_result, target_role)
for index, tip in enumerate(improvement_tips, start=1):
    st.write(f"**{index}.** {tip}")

# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    """
    🚀 AI Sustainable Career Intelligence Platform

    Resume Intelligence • Job Matching • Skill Gap Analysis
    • What-If Simulation • Project Recommendation
    • Career Roadmap • AI Career Advisor
    """
)


# ============================================================
# STEP 12 — AI JOB HUNTER AGENT
# ============================================================

st.header("🤖 Step 12 — AI Job Hunter Agent")
st.write(
    "Find live vacancies, filter irrelevant jobs, analyze promising jobs "
    "with Gemini, and rank the best opportunities for your resume."
)

# ------------------------------------------------------------
# Job Hunter imports
# ------------------------------------------------------------
try:
    from backend.database import init_db, SessionLocal
    from backend.models import Job
    from agent.job_sources import search_jobs
    from agent.matcher import is_relevant_job
    from agent.ai_matcher import analyze_job
except Exception as e:
    st.error(f"Job Hunter modules could not be loaded: {e}")
    st.stop()

# ------------------------------------------------------------
# Database initialization
# ------------------------------------------------------------
try:
    init_db()
except Exception as e:
    st.error(f"Could not initialize Job Hunter database: {e}")

# ------------------------------------------------------------
# Resume source
# ------------------------------------------------------------
job_hunter_resume = ""
job_hunter_name = "Candidate"

try:
    db = SessionLocal()
    profile = db.query(__import__("backend.models", fromlist=["Profile"]).Profile).first()

    if profile:
        job_hunter_resume = profile.resume_text or ""
        job_hunter_name = profile.name or "Candidate"

    db.close()
except Exception:
    pass

# Fallback to the resume already processed by the main app
if not job_hunter_resume:
    job_hunter_resume = resume_text

if not job_hunter_resume:
    st.warning("Upload or configure a resume before running the Job Hunter.")
else:
    st.success(f"Resume ready for Job Hunter: **{job_hunter_name}**")

# ------------------------------------------------------------
# Pipeline stage display
# ------------------------------------------------------------
st.subheader("🔄 Job Hunter Pipeline")

stage_col1, stage_col2, stage_col3, stage_col4 = st.columns(4)
with stage_col1:
    st.info("① 🔎\n\n**Find Jobs**\n\nLive job APIs")
with stage_col2:
    st.info("② 🧹\n\n**Filter Jobs**\n\nRemove obvious noise")
with stage_col3:
    st.info("③ 🤖\n\n**Gemini AI**\n\nResume ↔ Job analysis")
with stage_col4:
    st.info("④ 🏆\n\n**Rank Jobs**\n\nApply / Skip")

st.caption(
    "Current stage: live discovery → rule-based filtering → Gemini AI → ranking. "
    "Telegram approval and automatic application are not enabled yet."
)

# ------------------------------------------------------------
# Controls
# ------------------------------------------------------------
control_col1, control_col2, control_col3 = st.columns([2, 1, 1])

with control_col1:
    hunter_search = st.text_input(
        "Job search",
        value="AI Engineer",
        key="hunter_search_query"
    )

with control_col2:
    hunter_location = st.text_input(
        "Location",
        value="India",
        key="hunter_location_query"
    )

with control_col3:
    hunter_limit = st.number_input(
        "Jobs",
        min_value=1,
        max_value=20,
        value=5,
        step=1,
        key="hunter_limit"
    )

run_hunter = st.button(
    "🚀 Run AI Job Hunter",
    type="primary",
    use_container_width=True
)

# ------------------------------------------------------------
# Pipeline execution
# ------------------------------------------------------------
if run_hunter:

    if not job_hunter_resume:
        st.error("Resume is required before running the Job Hunter.")
        st.stop()

    # Clear previous results
    st.session_state.job_hunter_results = []
    st.session_state.job_hunter_stats = {}

    st.divider()
    st.subheader("📡 Stage 1 — Live Job Discovery")

    with st.status("Connecting to job sources...", expanded=True) as status:
        try:
            jobs_found = search_jobs(
                search=hunter_search,
                location=hunter_location,
                limit=int(hunter_limit)
            )

            st.write(f"✅ Jobs received from configured APIs: **{len(jobs_found)}**")

            for live_job in jobs_found:
                st.write(
                    f"• {live_job.get('title', 'Unknown')} — "
                    f"{live_job.get('company', 'Unknown company')}"
                )

            status.update(
                label=f"Stage 1 complete — {len(jobs_found)} jobs found",
                state="complete"
            )

        except Exception as e:
            status.update(label="Stage 1 failed", state="error")
            st.error(f"Job discovery failed: {e}")
            jobs_found = []

    # --------------------------------------------------------
    # Stage 2 — Local filter
    # --------------------------------------------------------
    st.subheader("🧹 Stage 2 — Local Relevance Filter")

    relevant_jobs = []
    filtered_jobs = []

    filter_progress = st.progress(0)

    total_live_jobs = len(jobs_found)

    for index, job in enumerate(jobs_found, start=1):
        title = job.get("title", "") or ""
        description = job.get("description", "") or ""

        result = is_relevant_job(
            job_hunter_resume,
            title,
            description
        )

        job["local_filter"] = result

        if result.get("relevant"):
            relevant_jobs.append(job)
        else:
            filtered_jobs.append(job)

        if total_live_jobs:
            filter_progress.progress(index / total_live_jobs)

    filter_progress.empty()

    filter_a, filter_b, filter_c = st.columns(3)
    filter_a.metric("Jobs Found", len(jobs_found))
    filter_b.metric("Passed Filter", len(relevant_jobs))
    filter_c.metric("Filtered Out", len(filtered_jobs))

    if relevant_jobs:
        filter_rows = []
        for job in relevant_jobs:
            local_result = job["local_filter"]
            filter_rows.append({
                "Job": job.get("title", "Unknown"),
                "Company": job.get("company", "Unknown"),
                "Local Score": local_result.get("relevance_score", 0),
                "Matched Skills": ", ".join(
                    local_result.get("matched_skills", [])
                )
            })

        st.dataframe(
            pd.DataFrame(filter_rows),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No jobs passed the local relevance filter.")

    # --------------------------------------------------------
    # Stage 3 — Gemini
    # --------------------------------------------------------
    st.subheader("🤖 Stage 3 — Gemini AI Job Analysis")

    ai_results = []
    ai_progress = st.progress(0)
    ai_status = st.empty()

    total_relevant = len(relevant_jobs)

    for index, job in enumerate(relevant_jobs, start=1):

        title = job.get("title", "Unknown")
        company = job.get("company", "Unknown")

        ai_status.info(
            f"Analyzing {index}/{total_relevant}: **{title}** — {company}"
        )

        try:
            ai_result = analyze_job(
                resume_text=job_hunter_resume,
                job_title=title,
                job_description=job.get("description", "") or ""
            )
        except TypeError:
            # Supports the current analyzer if it uses positional arguments.
            ai_result = analyze_job(
                job_hunter_resume,
                title,
                job.get("description", "") or ""
            )
        except Exception as e:
            ai_result = {
                "success": False,
                "score": None,
                "recommendation": "AI_ERROR",
                "reason": "Gemini analysis failed.",
                "strengths": [],
                "missing_skills": [],
                "error": str(e)
            }

        ai_results.append({
            "job": job,
            "ai": ai_result
        })

        if total_relevant:
            ai_progress.progress(index / total_relevant)

    ai_progress.empty()
    ai_status.empty()

    # --------------------------------------------------------
    # Stage 4 — Ranking
    # --------------------------------------------------------
    st.subheader("🏆 Stage 4 — Final AI Job Ranking")

    successful_results = []
    failed_results = []

    for item in ai_results:
        ai_result = item["ai"]
        score = ai_result.get("score")

        if ai_result.get("success") and score is not None:
            successful_results.append(item)
        else:
            failed_results.append(item)

    successful_results.sort(
        key=lambda item: float(item["ai"].get("score", 0) or 0),
        reverse=True
    )

    st.session_state.job_hunter_results = successful_results
    st.session_state.job_hunter_stats = {
        "found": len(jobs_found),
        "relevant": len(relevant_jobs),
        "successful": len(successful_results),
        "failed": len(failed_results)
    }

    if successful_results:

        ranking_rows = []

        for rank, item in enumerate(successful_results, start=1):
            job = item["job"]
            ai_result = item["ai"]

            ranking_rows.append({
                "Rank": rank,
                "Job": job.get("title", "Unknown"),
                "Company": job.get("company", "Unknown"),
                "AI Score": float(ai_result.get("score", 0)),
                "Recommendation": ai_result.get(
                    "recommendation", "Unknown"
                )
            })

        ranking_df = pd.DataFrame(ranking_rows)

        st.dataframe(
            ranking_df,
            use_container_width=True,
            hide_index=True
        )

        # Highlight best job
        best = successful_results[0]
        best_job = best["job"]
        best_ai = best["ai"]
        best_score = float(best_ai.get("score", 0))

        if best_score >= 70:
            st.success(
                f"🥇 Best current opportunity: **{best_job.get('title', 'Unknown')}** "
                f"at **{best_job.get('company', 'Unknown')}** — "
                f"**{best_score:.1f}/100**"
            )
        elif best_score >= 50:
            st.warning(
                f"🥇 Best current opportunity: **{best_job.get('title', 'Unknown')}** "
                f"— **{best_score:.1f}/100**. Review before applying."
            )
        else:
            st.info(
                f"No strong match found. Highest score: **{best_score:.1f}/100**."
            )

        # Detailed result cards
        for rank, item in enumerate(successful_results, start=1):
            job = item["job"]
            ai_result = item["ai"]
            score = float(ai_result.get("score", 0) or 0)
            recommendation = ai_result.get("recommendation", "Unknown")

            with st.expander(
                f"#{rank} — {job.get('title', 'Unknown')} | "
                f"{job.get('company', 'Unknown')} | {score:.1f}/100"
            ):
                detail_col1, detail_col2 = st.columns(2)

                with detail_col1:
                    st.metric("Gemini Match Score", f"{score:.1f}/100")
                    st.write(f"**Recommendation:** {recommendation}")
                    st.write(
                        f"**Source:** {job.get('source', 'Unknown')}"
                    )
                    if job.get("job_url"):
                        st.link_button(
                            "🔗 Open Job Vacancy",
                            job["job_url"]
                        )

                with detail_col2:
                    st.write("**Strengths**")
                    strengths = ai_result.get("strengths", []) or []
                    if strengths:
                        for strength in strengths:
                            st.write(f"✅ {strength}")
                    else:
                        st.write("No strengths returned.")

                st.write("**AI Reason**")
                st.write(
                    ai_result.get(
                        "reason",
                        "No reason returned."
                    )
                )

                st.write("**Missing Skills / Requirements**")
                missing = ai_result.get("missing_skills", []) or []
                if missing:
                    for skill in missing:
                        st.write(f"❌ {skill}")
                else:
                    st.success("No major missing requirements returned.")

    else:
        st.warning("Gemini did not produce a successful analysis for the filtered jobs.")

    if failed_results:
        st.warning(
            f"{len(failed_results)} job(s) could not be analyzed by Gemini."
        )

    # --------------------------------------------------------
    # Current progress summary
    # --------------------------------------------------------
    st.divider()
    st.subheader("📊 Job Hunter Run Summary")

    summary = st.session_state.job_hunter_stats
    s1, s2, s3, s4 = st.columns(4)

    with s1:
        st.metric("Jobs Collected", summary.get("found", 0))
    with s2:
        st.metric("Passed Filter", summary.get("relevant", 0))
    with s3:
        st.metric("Gemini Success", summary.get("successful", 0))
    with s4:
        st.metric("AI Failures", summary.get("failed", 0))

# ------------------------------------------------------------
# Show previous run after Streamlit rerun
# ------------------------------------------------------------
elif st.session_state.get("job_hunter_results"):

    st.subheader("📌 Last Job Hunter Results")

    previous_results = st.session_state.job_hunter_results

    for rank, item in enumerate(previous_results, start=1):
        job = item["job"]
        ai_result = item["ai"]
        score = float(ai_result.get("score", 0) or 0)

        st.write(
            f"**#{rank} {job.get('title', 'Unknown')}** — "
            f"{job.get('company', 'Unknown')} — **{score:.1f}/100** — "
            f"{ai_result.get('recommendation', 'Unknown')}"
        )

st.info(
    "🚧 Next Job Hunter stages: Telegram approval → resume tailoring → "
    "cover letter → controlled application automation → application tracking."
)
