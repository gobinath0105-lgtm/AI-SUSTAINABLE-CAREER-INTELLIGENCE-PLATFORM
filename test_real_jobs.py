from backend.database import (
    SessionLocal,
    init_db,
)

from backend.models import Job
from agent.ai_matcher import analyze_job


# ============================================================
# INITIALIZE DATABASE
# ============================================================

init_db()

db = SessionLocal()


# ============================================================
# TEST RESUME
# ============================================================

resume_text = """
B.Tech Artificial Intelligence and Data Science student.

Skills:
Python, SQL, Machine Learning, Deep Learning,
TensorFlow, NLP, RAG, Git, Pandas.

Projects:
House Price Prediction,
Customer Churn Prediction,
MNIST CNN,
Cat vs Dog Classification.
"""


# ============================================================
# GET REAL JOBS
# ============================================================

jobs = (
    db.query(Job)
    .order_by(Job.discovered_at.desc())
    .limit(5)
    .all()
)


print()
print("=" * 70)
print("AI JOB HUNTER - REAL JOB ANALYSIS")
print("=" * 70)

print()
print(f"Jobs found in database: {len(jobs)}")


if not jobs:

    print()
    print("No jobs found in database.")
    print("Run test_job_sources.py first.")

    db.close()
    exit()


# ============================================================
# ANALYZE EACH JOB
# ============================================================

results = []


for index, job in enumerate(jobs, start=1):

    print()
    print("-" * 70)

    print(
        f"[{index}/{len(jobs)}] "
        f"{job.title}"
    )

    print(
        f"Company: {job.company}"
    )

    print(
        f"Source: {job.source}"
    )

    print()
    print("Sending to Gemini...")

    result = analyze_job(
        resume_text=resume_text,
        job_title=job.title,
        job_description=job.description or "",
        job_company=job.company or "",
    )

    results.append(
        {
            "job": job,
            "result": result,
        }
    )


# ============================================================
# RANK JOBS
# ============================================================

results.sort(
    key=lambda item: item["result"]["score"],
    reverse=True
)


# ============================================================
# DISPLAY RANKING
# ============================================================

print()
print()
print("=" * 70)
print("🔥 AI JOB RANKING")
print("=" * 70)

for rank, item in enumerate(
    results,
    start=1
):

    job = item["job"]
    result = item["result"]

    print()
    print(
        f"#{rank} {job.title}"
    )

    print(
        f"Company: {job.company}"
    )

    print(
        f"AI Match Score: "
        f"{result['score']}/100"
    )

    print(
        f"Recommendation: "
        f"{result['recommendation']}"
    )

    print(
        f"Reason: "
        f"{result['reason']}"
    )

    print(
        "Missing Skills: "
        + (
            ", ".join(
                result["missing_skills"]
            )
            if result["missing_skills"]
            else "None"
        )
    )


# ============================================================
# CLOSE DATABASE
# ============================================================

db.close()

print()
print("=" * 70)
print("REAL JOB ANALYSIS COMPLETED")
print("=" * 70)