
from pathlib import Path

from backend.database import (
    init_db,
    SessionLocal,
    create_or_update_profile
)


# ============================================================
# CONFIGURATION
# ============================================================

RESUME_TEXT_PATH = "resume_text.txt"


# ============================================================
# MAIN
# ============================================================

print("=" * 60)
print("CLEAN RESUME TEST")
print("=" * 60)


# ============================================================
# CHECK FILE
# ============================================================

if not Path(RESUME_TEXT_PATH).exists():

    print("\nresume_text.txt not found!")

    print("\nCreate this file inside:")
    print("AI resume project/")
    print("└── resume_text.txt")

    exit()


print("\nClean resume found!")


# ============================================================
# READ RESUME
# ============================================================

resume_text = Path(
    RESUME_TEXT_PATH
).read_text(
    encoding="utf-8"
)


print("\nResume loaded successfully!")

print("\nCharacter count:", len(resume_text))

print("\nFirst 1000 characters:")
print("-" * 60)

print(resume_text[:1000])

print("-" * 60)


# ============================================================
# SAVE TO DATABASE
# ============================================================

print("\nSaving clean resume to SQLite...")

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

        resume_path=RESUME_TEXT_PATH,

        resume_text=resume_text
    )

    print("\nClean resume saved to SQLite!")

    print("Profile ID:", profile.id)

    print("Resume text saved:", len(profile.resume_text), "characters")


finally:

    db.close()


print("\n" + "=" * 60)
print("CLEAN RESUME INTEGRATION SUCCESSFUL")
print("=" * 60)
