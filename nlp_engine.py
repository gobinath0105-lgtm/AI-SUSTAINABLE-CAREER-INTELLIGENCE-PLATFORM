# ============================================================
# NLP ENGINE
# ============================================================

import re
from collections import Counter


# ------------------------------------------------------------
# CLEAN TEXT
# ------------------------------------------------------------

def clean_text(text):

    if text is None:
        return ""

    text = str(text)

    # Fix PDF broken words
    text = re.sub(
        r"-\s*\n\s*",
        "",
        text
    )

    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ------------------------------------------------------------
# SENTENCE ANALYSIS
# ------------------------------------------------------------

def analyze_sentences(text):

    text = clean_text(text)

    if not text:
        return {
            "sentence_count": 0,
            "average_sentence_length": 0,
            "long_sentences": 0,
            "short_sentences": 0
        }

    sentences = re.split(
        r"[.!?]+",
        text
    )

    sentences = [
        s.strip()
        for s in sentences
        if s.strip()
    ]

    if not sentences:

        return {
            "sentence_count": 0,
            "average_sentence_length": 0,
            "long_sentences": 0,
            "short_sentences": 0
        }

    lengths = []

    for sentence in sentences:

        words = re.findall(
            r"\b\w+\b",
            sentence
        )

        lengths.append(len(words))

    average_length = (
        sum(lengths) / len(lengths)
    )

    long_sentences = sum(
        1 for length in lengths
        if length > 30
    )

    short_sentences = sum(
        1 for length in lengths
        if length < 5
    )

    return {

        "sentence_count": len(sentences),

        "average_sentence_length": round(
            average_length,
            1
        ),

        "long_sentences": long_sentences,

        "short_sentences": short_sentences
    }


# ------------------------------------------------------------
# WORD STATISTICS
# ------------------------------------------------------------

def analyze_words(text):

    text = clean_text(text)

    words = re.findall(
        r"\b[a-zA-Z][a-zA-Z0-9+#.-]*\b",
        text.lower()
    )

    if not words:

        return {
            "word_count": 0,
            "unique_words": 0,
            "vocabulary_diversity": 0,
            "top_words": []
        }

    unique_words = set(words)

    diversity = (
        len(unique_words) / len(words)
    ) * 100

    stop_words = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "this",
        "that",
        "have",
        "has",
        "are",
        "was",
        "were",
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
        "also"
    }

    filtered_words = [
        word
        for word in words
        if word not in stop_words
        and len(word) > 2
    ]

    counter = Counter(filtered_words)

    top_words = counter.most_common(10)

    return {

        "word_count": len(words),

        "unique_words": len(unique_words),

        "vocabulary_diversity": round(
            diversity,
            1
        ),

        "top_words": top_words
    }


# ------------------------------------------------------------
# RESUME SECTIONS
# ------------------------------------------------------------

def detect_resume_sections(text):

    text = clean_text(text).lower()

    sections = {

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
            "certification",
            "certifications",
            "certificate",
            "certificates"
        ],

        "Achievements": [
            "achievement",
            "achievements",
            "awards"
        ]
    }

    result = {}

    for section, keywords in sections.items():

        found = False

        for keyword in keywords:

            if keyword in text:
                found = True
                break

        result[section] = found

    return result


# ------------------------------------------------------------
# SKILL EVIDENCE
# ------------------------------------------------------------

def find_skill_evidence(
    resume_text,
    skills,
    skill_aliases=None
):

    text = clean_text(resume_text).lower()

    evidence = {}

    for skill in skills:

        skill_lower = str(skill).lower()

        patterns = [
            skill_lower
        ]

        if skill_aliases:

            for alias, standard in skill_aliases.items():

                if str(standard).lower() == skill_lower:
                    patterns.append(
                        str(alias).lower()
                    )

        found_sentences = []

        sentences = re.split(
            r"[.!?\n]+",
            resume_text
        )

        for sentence in sentences:

            sentence_lower = sentence.lower()

            for pattern in patterns:

                if pattern in sentence_lower:

                    clean_sentence = sentence.strip()

                    if clean_sentence:
                        found_sentences.append(
                            clean_sentence
                        )

                    break

        if found_sentences:

            evidence[skill] = found_sentences[:3]

    return evidence


# ------------------------------------------------------------
# NLP SCORE
# ------------------------------------------------------------

def calculate_nlp_score(
    resume_text,
    skills=None,
    skill_aliases=None
):

    resume_text = clean_text(resume_text)

    if not resume_text:

        return {
            "nlp_score": 0,
            "word_stats": {},
            "sentence_stats": {},
            "sections": {},
            "skill_evidence": {},
            "recommendations": []
        }

    word_stats = analyze_words(
        resume_text
    )

    sentence_stats = analyze_sentences(
        resume_text
    )

    sections = detect_resume_sections(
        resume_text
    )

    skills = skills or []

    skill_evidence = find_skill_evidence(
        resume_text,
        skills,
        skill_aliases
    )

    score = 0

    # Word quality
    if word_stats["word_count"] >= 250:
        score += 30

    elif word_stats["word_count"] >= 150:
        score += 20

    else:
        score += 10

    # Vocabulary
    if word_stats["vocabulary_diversity"] >= 50:
        score += 25

    elif word_stats["vocabulary_diversity"] >= 35:
        score += 18

    else:
        score += 10

    # Sentence quality
    if sentence_stats["average_sentence_length"] <= 30:
        score += 20

    else:
        score += 10

    # Sections
    important_sections = [
        "Education",
        "Skills",
        "Projects",
        "Experience"
    ]

    section_count = sum(
        1
        for section in important_sections
        if sections.get(section, False)
    )

    score += (
        section_count / len(important_sections)
    ) * 25

    score = round(
        min(100, score),
        1
    )

    recommendations = []

    if word_stats["word_count"] < 250:
        recommendations.append(
            "Add more useful details about your projects and technical experience."
        )

    if word_stats["vocabulary_diversity"] < 35:
        recommendations.append(
            "Avoid repeating the same words too often."
        )

    if sentence_stats["long_sentences"] > 3:
        recommendations.append(
            "Break long sentences into shorter, clearer statements."
        )

    if not sections.get("Projects", False):
        recommendations.append(
            "Add a Projects section to demonstrate practical work."
        )

    if not sections.get("Skills", False):
        recommendations.append(
            "Add a clear Technical Skills section."
        )

    if not recommendations:
        recommendations.append(
            "Your resume has good basic NLP structure and readability."
        )

    return {

        "nlp_score": score,

        "word_stats": word_stats,

        "sentence_stats": sentence_stats,

        "sections": sections,

        "skill_evidence": skill_evidence,

        "recommendations": recommendations
    }