# ============================================================
# ATS ENGINE
# ============================================================

import re


# ------------------------------------------------------------
# TEXT CLEANING
# ------------------------------------------------------------

def clean_text(text):
    if text is None:
        return ""

    text = str(text)

    # Fix PDF line breaks
    text = re.sub(r"-\s*\n\s*", "", text)

    # Replace newlines/tabs with spaces
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")

    # Normalize spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ------------------------------------------------------------
# NORMALIZE SKILL
# ------------------------------------------------------------

def normalize_skill(skill):
    skill = str(skill).lower().strip()

    skill = skill.replace("&", " and ")
    skill = skill.replace("/", " ")
    skill = skill.replace("-", " ")
    skill = skill.replace("_", " ")

    skill = re.sub(r"\s+", " ", skill)

    return skill.strip()


# ------------------------------------------------------------
# SKILL MATCHING
# ------------------------------------------------------------

def skill_exists(resume_text, skill, skill_aliases=None):

    resume = normalize_skill(resume_text)
    target = normalize_skill(skill)

    if not resume or not target:
        return False

    # Direct match
    pattern = r"(?<![a-z0-9])" + re.escape(target) + r"(?![a-z0-9])"

    if re.search(pattern, resume):
        return True

    # Alias matching
    if skill_aliases:

        for alias, standard_skill in skill_aliases.items():

            if normalize_skill(standard_skill) == target:

                alias_clean = normalize_skill(alias)

                alias_pattern = (
                    r"(?<![a-z0-9])"
                    + re.escape(alias_clean)
                    + r"(?![a-z0-9])"
                )

                if re.search(alias_pattern, resume):
                    return True

    return False


# ------------------------------------------------------------
# FIND MATCHED SKILLS
# ------------------------------------------------------------

def get_skill_match(resume_text, required_skills, skill_aliases=None):

    matched = []
    missing = []

    for skill in required_skills:

        if skill_exists(
            resume_text,
            skill,
            skill_aliases
        ):
            matched.append(skill)

        else:
            missing.append(skill)

    return matched, missing


# ------------------------------------------------------------
# SECTION DETECTION
# ------------------------------------------------------------

def detect_sections(resume_text):

    text = clean_text(resume_text).lower()

    section_keywords = {

        "Contact Information": [
            "email",
            "phone",
            "mobile",
            "linkedin",
            "github"
        ],

        "Summary": [
            "summary",
            "profile",
            "objective",
            "career objective"
        ],

        "Education": [
            "education",
            "academic",
            "degree",
            "b.tech",
            "bachelor",
            "master"
        ],

        "Skills": [
            "skills",
            "technical skills",
            "technologies",
            "tools"
        ],

        "Experience": [
            "experience",
            "work experience",
            "professional experience",
            "internship"
        ],

        "Projects": [
            "projects",
            "project"
        ],

        "Certifications": [
            "certifications",
            "certificates",
            "certification"
        ],

        "Achievements": [
            "achievements",
            "awards",
            "accomplishments"
        ]
    }

    results = {}

    for section, keywords in section_keywords.items():

        found = False

        for keyword in keywords:

            pattern = r"\b" + re.escape(keyword.lower()) + r"\b"

            if re.search(pattern, text):
                found = True
                break

        results[section] = found

    return results


# ------------------------------------------------------------
# KEYWORD EXTRACTION
# ------------------------------------------------------------

def extract_keywords(resume_text):

    text = clean_text(resume_text).lower()

    common_words = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "this",
        "that",
        "have",
        "has",
        "was",
        "were",
        "are",
        "you",
        "your",
        "our",
        "into",
        "using",
        "used",
        "will",
        "can",
        "not",
        "but",
        "all",
        "about",
        "their",
        "they",
        "been",
        "also",
        "which",
        "who",
        "how",
        "what",
        "when",
        "where"
    }

    words = re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.-]{2,}\b", text)

    keywords = []

    for word in words:

        word = word.lower().strip(".,;:()[]{}")

        if len(word) < 3:
            continue

        if word in common_words:
            continue

        if word not in keywords:
            keywords.append(word)

    return keywords


# ------------------------------------------------------------
# ATS SCORE
# ------------------------------------------------------------

def calculate_ats_score(
    resume_text,
    target_role=None,
    role_skills=None,
    skill_aliases=None
):

    resume_text = clean_text(resume_text)

    if not resume_text:

        return {
            "ats_score": 0,
            "skill_coverage": 0,
            "skill_score": 0,
            "keyword_coverage": 0,
            "keyword_score": 0,
            "content_score": 0,
            "content_points": 0,
            "section_score": 0,
            "section_points": 0,
            "word_count": 0,
            "matched_role_skills": [],
            "missing_role_skills": [],
            "section_results": {},
            "recommendations": []
        }

    # --------------------------------------------------------
    # WORD COUNT
    # --------------------------------------------------------

    words = re.findall(r"\b\w+\b", resume_text)

    word_count = len(words)

    # --------------------------------------------------------
    # ROLE SKILLS
    # --------------------------------------------------------

    role_skills = role_skills or []

    matched_role_skills, missing_role_skills = get_skill_match(
        resume_text,
        role_skills,
        skill_aliases
    )

    if role_skills:

        skill_coverage = (
            len(matched_role_skills)
            / len(role_skills)
        ) * 100

    else:

        skill_coverage = 0

    skill_score = round(skill_coverage, 1)

    # --------------------------------------------------------
    # KEYWORDS
    # --------------------------------------------------------

    keywords = extract_keywords(resume_text)

    if keywords:

        keyword_score = min(
            100,
            40 + (len(keywords) * 1.5)
        )

    else:

        keyword_score = 0

    keyword_score = round(keyword_score, 1)

    keyword_coverage = keyword_score

    # --------------------------------------------------------
    # CONTENT SCORE
    # --------------------------------------------------------

    content_points = 0

    if 250 <= word_count <= 900:
        content_points += 40

    elif 150 <= word_count < 250:
        content_points += 25

    elif 900 < word_count <= 1200:
        content_points += 30

    elif word_count > 1200:
        content_points += 20

    else:
        content_points += 10

    # Action verbs
    action_verbs = [
        "developed",
        "built",
        "created",
        "implemented",
        "designed",
        "trained",
        "deployed",
        "optimized",
        "analyzed",
        "developed",
        "automated",
        "improved",
        "integrated",
        "managed",
        "tested"
    ]

    lower_resume = resume_text.lower()

    action_count = sum(
        1 for verb in action_verbs
        if re.search(
            r"\b" + re.escape(verb) + r"\b",
            lower_resume
        )
    )

    if action_count >= 5:
        content_points += 30

    elif action_count >= 3:
        content_points += 20

    elif action_count >= 1:
        content_points += 10

    # Numbers / measurable achievements
    numbers = re.findall(
        r"\b\d+(?:\.\d+)?%?\b",
        resume_text
    )

    if len(numbers) >= 5:
        content_points += 30

    elif len(numbers) >= 2:
        content_points += 20

    else:
        content_points += 10

    content_score = min(100, content_points)

    # --------------------------------------------------------
    # SECTIONS
    # --------------------------------------------------------

    section_results = detect_sections(resume_text)

    important_sections = [
        "Contact Information",
        "Summary",
        "Education",
        "Skills",
        "Experience",
        "Projects"
    ]

    section_points = sum(
        1
        for section in important_sections
        if section_results.get(section, False)
    )

    section_score = (
        section_points / len(important_sections)
    ) * 100

    section_score = round(section_score, 1)

    # --------------------------------------------------------
    # FINAL ATS SCORE
    # --------------------------------------------------------

    ats_score = (
        skill_score * 0.45
        + keyword_score * 0.15
        + content_score * 0.20
        + section_score * 0.20
    )

    ats_score = round(
        max(0, min(100, ats_score)),
        1
    )

    # --------------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------------

    recommendations = []

    if skill_score < 60:
        recommendations.append(
            "Add more skills required for the selected target role."
        )

    if keyword_score < 60:
        recommendations.append(
            "Add relevant technical keywords naturally inside your resume."
        )

    if section_score < 80:
        recommendations.append(
            "Add missing resume sections such as Projects, Skills, Education or Experience."
        )

    if content_score < 60:
        recommendations.append(
            "Improve project descriptions using action verbs and measurable results."
        )

    if word_count < 250:
        recommendations.append(
            "Your resume is short. Add stronger project, skills and experience details."
        )

    if word_count > 1200:
        recommendations.append(
            "Your resume is long. Remove unnecessary information."
        )

    if not recommendations:
        recommendations.append(
            "Your resume has a strong overall ATS structure."
        )

    return {

        "ats_score": ats_score,

        "skill_coverage": round(skill_coverage, 1),

        "skill_score": skill_score,

        "keyword_coverage": keyword_coverage,

        "keyword_score": keyword_score,

        "content_score": content_score,

        "content_points": content_points,

        "section_score": section_score,

        "section_points": section_points,

        "word_count": word_count,

        "matched_role_skills": matched_role_skills,

        "missing_role_skills": missing_role_skills,

        "section_results": section_results,

        "recommendations": recommendations
    }