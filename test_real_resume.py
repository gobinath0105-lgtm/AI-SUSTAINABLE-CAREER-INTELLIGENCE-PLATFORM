from pathlib import Path
from pypdf import PdfReader
import re

from backend.database import (
    init_db,
    SessionLocal,
    create_or_update_profile
)


# ============================================================
# CONFIGURATION
# ============================================================

RESUME_PATH = "Gobinath_Resume.pdf"


# ============================================================
# TEXT CLEANING
# ============================================================

def clean_line(line):
    """
    Clean one line extracted from the PDF.
    """

    line = line.strip()

    if not line:
        return ""

    # --------------------------------------------------------
    # Fix character-spaced words
    #
    # Example:
    # "P y t h o n" -> "Python"
    # "N L P"       -> "NLP"
    # "G O B I N A T H" -> "GOBINATH"
    # --------------------------------------------------------

    tokens = line.split()

    cleaned_tokens = []

    i = 0

    while i < len(tokens):

        token = tokens[i]

        # Single alphabetic character
        if len(token) == 1 and token.isalpha():

            chars = [token]

            j = i + 1

            while j < len(tokens):

                next_token = tokens[j]

                if len(next_token) == 1 and next_token.isalpha():
                    chars.append(next_token)
                    j += 1
                else:
                    break

            # Combine character sequence
            if len(chars) >= 2:

                cleaned_tokens.append("".join(chars))

                i = j

            else:

                cleaned_tokens.append(token)

                i += 1

        else:

            cleaned_tokens.append(token)

            i += 1

    line = " ".join(cleaned_tokens)

    # --------------------------------------------------------
    # Fix common spacing around punctuation
    # --------------------------------------------------------

    line = re.sub(r"\s+@", "@", line)
    line = re.sub(r"@\s+", "@", line)

    line = re.sub(r"\s+\.", ".", line)
    line = re.sub(r"\.\s+", ".", line)

    line = re.sub(r"\s+/", "/", line)
    line = re.sub(r"/\s+", "/", line)

    line = re.sub(r"\s+-\s+", "-", line)

    # --------------------------------------------------------
    # Fix phone number
    #
    # Example:
    # 8 0 9 8 0 1 3 8 2 9
    # becomes:
    # 8098013829
    # --------------------------------------------------------

    line = re.sub(
        r"(?<!\d)(?:\d\s+){8,}\d(?!\d)",
        lambda match: match.group(0).replace(" ", ""),
        line
    )

    # --------------------------------------------------------
    # Remove repeated spaces
    # --------------------------------------------------------

    line = re.sub(r"\s+", " ", line).strip()

    return line


# ============================================================
# EXTRACT RESUME TEXT
# ============================================================

def extract_resume_text(pdf_path):

    reader = PdfReader(pdf_path)

    cleaned_pages = []

    for page in reader.pages:

        raw_text = page.extract_text()

        if not raw_text:
            continue

        # Process line by line
        raw_lines = raw_text.splitlines()

        page_lines = []

        for raw_line in raw_lines:

            cleaned = clean_line(raw_line)

            if cleaned:
                page_lines.append(cleaned)

        cleaned_pages.append("\n".join(page_lines))

    # Combine pages
    resume_text = "\n".join(cleaned_pages)

    # --------------------------------------------------------
    # Additional fixes for common PDF word separation
    # --------------------------------------------------------

    # Fix common technology names
    replacements = {
        "Scikit -learn": "Scikit-learn",
        "Tensor Flow": "TensorFlow",
        "Keras": "Keras",
        "Machine Learning": "Machine Learning",
        "Deep Learning": "Deep Learning",
        "Artificial Intelligence": "Artificial Intelligence",
        "Data Science": "Data Science",
        "Object -Oriented": "Object-Oriented",
        "Real -world": "Real-world",
        "CNN -based": "CNN-based",
    }

    for old, new in replacements.items():
        resume_text = resume_text.replace(old, new)

    # --------------------------------------------------------
    # Final whitespace cleanup
    # --------------------------------------------------------

    resume_text = re.sub(
        r"[ \t]+",
        " ",
        resume_text
    )

    resume_text = re.sub(
        r"\n{2,}",
        "\n",
        resume_text
    )

    return resume_text.strip()


# ============================================================
# MAIN
# ============================================================

print("=" * 60)
print("REAL RESUME TEST")
print("=" * 60)


# ============================================================
# CHECK FILE
# ============================================================

if not Path(RESUME_PATH).exists():

    print()
    print("Resume PDF not found!")
    print()
    print("Make sure this file exists:")
    print()
    print("AI resume project/")
    print("└── Gobinath_Resume.pdf")
    print()

    exit()


print()
print("Resume found!")


# ============================================================
# EXTRACT
# ============================================================

resume_text = extract_resume_text(RESUME_PATH)


print()
print("Resume text extracted successfully!")

print()
print("Character count:", len(resume_text))


# ============================================================
# SHOW EXTRACTED TEXT
# ============================================================

print()
print("Cleaned resume text:")
print("-" * 60)

print(resume_text[:2000])

print("-" * 60)


# ============================================================
# SAVE TO DATABASE
# ============================================================

print()
print("Saving resume profile to SQLite...")

init_db()

db = SessionLocal()

try:

    profile = create_or_update_profile(
        db,

        name="Gobinath",

        email="gobinath0105@gmail.com",

        phone="8098013829",

        location="Udumalpet, Tamil Nadu, India",

        roles=(
            "AI Engineer,"
            "NLP Engineer,"
            "GenAI Engineer,"
            "AI/ML Intern"
        ),

        skills=(
            "Python,"
            "SQL,"
            "Machine Learning,"
            "Deep Learning,"
            "TensorFlow,"
            "Keras,"
            "NLP,"
            "LLM,"
            "Embeddings,"
            "RAG,"
            "LangChain,"
            "Scikit-learn,"
            "Pandas,"
            "Matplotlib,"
            "Transformers,"
            "CNN,"
            "RNN,"
            "LSTM,"
            "FastAPI,"
            "Flask,"
            "OpenCV,"
            "YOLO,"
            "Git,"
            "GitHub"
        ),

        minimum_salary=0,

        remote_only=False,

        resume_path=RESUME_PATH,

        resume_text=resume_text
    )

    print()
    print("Resume profile saved to SQLite!")

    print()
    print("Profile ID:", profile.id)
    print("Name:", profile.name)
    print("Resume path:", profile.resume_path)

    print(
        "Resume text saved:",
        len(profile.resume_text),
        "characters"
    )

finally:

    db.close()


# ============================================================
# SUCCESS
# ============================================================

print()
print("=" * 60)
print("REAL RESUME INTEGRATION SUCCESSFUL")
print("=" * 60)