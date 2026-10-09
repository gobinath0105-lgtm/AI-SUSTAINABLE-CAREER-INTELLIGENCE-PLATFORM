from agent.job_sources import search_jobs
from backend.database import init_db, SessionLocal, add_job
from backend.models import Job


print("Starting job hunter test...")
print()


# ============================================================
# 1. CREATE DATABASE
# ============================================================

init_db()

print("Database ready.")
print()


# ============================================================
# 2. FETCH JOBS
# ============================================================

jobs = search_jobs(
    search="AI Engineer",
    location="India",
    limit=5
)

print(f"Jobs fetched: {len(jobs)}")
print()


# ============================================================
# 3. SAVE JOBS
# ============================================================

db = SessionLocal()

try:

    saved_count = 0
    duplicate_count = 0

    for job_data in jobs:

        # Check whether job already exists
        existing_job = (
            db.query(Job)
            .filter(
                Job.external_id
                == job_data["external_id"]
            )
            .first()
        )

        if existing_job:

            duplicate_count += 1

            print(
                f"Duplicate skipped: "
                f"{job_data['title']}"
            )

            continue

        # Create database Job object
        job = Job(
            external_id=job_data["external_id"],
            source=job_data["source"],
            title=job_data["title"],
            company=job_data["company"],
            location=job_data["location"],
            description=job_data["description"],
            job_url=job_data["job_url"],
            salary_min=job_data["salary_min"],
            salary_max=job_data["salary_max"],
            remote=job_data["remote"],
            published_at=job_data["published_at"]
        )

        add_job(
            db,
            job
        )

        saved_count += 1

        print(
            f"Saved: "
            f"{job_data['title']}"
        )

    print()
    print("=" * 60)
    print("JOB HUNTER RESULT")
    print("=" * 60)
    print(f"Fetched jobs   : {len(jobs)}")
    print(f"New jobs saved : {saved_count}")
    print(f"Duplicates     : {duplicate_count}")
    print("=" * 60)

finally:

    db.close()