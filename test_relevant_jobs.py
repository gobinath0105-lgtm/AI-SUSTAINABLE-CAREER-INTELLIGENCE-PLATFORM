from backend.database import init_db, SessionLocal
from backend.models import Job, Profile
from agent.matcher import is_relevant_job


# ============================================================
# START
# ============================================================

print("=" * 70)
print("REAL RESUME + REAL JOB RELEVANCE FILTER")
print("=" * 70)


# ============================================================
# INITIALIZE DATABASE
# ============================================================

init_db()

db = SessionLocal()


try:

    # --------------------------------------------------------
    # GET PROFILE
    # --------------------------------------------------------

    profile = (
        db.query(Profile)
        .order_by(Profile.id.asc())
        .first()
    )

    if not profile:

        print("\nNo resume profile found!")

        print(
            "Run test_clean_resume.py first."
        )

        exit()

    print("\nResume profile found!")

    print("Name:", profile.name)

    print(
        "Resume characters:",
        len(profile.resume_text)
    )


    # --------------------------------------------------------
    # GET JOBS
    # --------------------------------------------------------

    jobs = (
        db.query(Job)
        .order_by(Job.discovered_at.desc())
        .all()
    )

    print(
        "\nJobs in database:",
        len(jobs)
    )


    if not jobs:

        print("\nNo jobs found in database.")

        print(
            "Run test_job_sources.py first."
        )

        exit()


    # ========================================================
    # FILTER JOBS
    # ========================================================

    relevant_jobs = []

    rejected_jobs = []


    print("\n" + "=" * 70)
    print("CHECKING JOB RELEVANCE")
    print("=" * 70)


    for job in jobs:

        result = is_relevant_job(
            resume_text=profile.resume_text,
            job_title=job.title,
            job_description=job.description or ""
        )


        job_result = {
            "job": job,
            "result": result
        }


        if result["relevant"]:

            relevant_jobs.append(
                job_result
            )

        else:

            rejected_jobs.append(
                job_result
            )


    # ========================================================
    # SORT BY RELEVANCE SCORE
    # ========================================================

    relevant_jobs.sort(
        key=lambda item: item["result"]["relevance_score"],
        reverse=True
    )


    # ========================================================
    # SHOW RELEVANT JOBS
    # ========================================================

    print("\n")
    print("=" * 70)
    print("🔥 RELEVANT JOBS")
    print("=" * 70)


    if not relevant_jobs:

        print("\nNo relevant jobs found.")

    else:

        for index, item in enumerate(
            relevant_jobs,
            start=1
        ):

            job = item["job"]
            result = item["result"]


            print(
                f"\n#{index} {job.title}"
            )

            print(
                "Company:",
                job.company
            )

            print(
                "Source:",
                job.source
            )

            print(
                "Relevance Score:",
                result["relevance_score"]
            )

            print(
                "Matched Skills:",
                ", ".join(
                    result["matched_skills"]
                )
            )

            print(
                "Reason:",
                result["reason"]
            )

            print(
                "URL:",
                job.job_url
            )


    # ========================================================
    # SHOW REJECTED JOB COUNT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("FILTER SUMMARY")
    print("=" * 70)

    print(
        "\nTotal jobs:",
        len(jobs)
    )

    print(
        "Relevant jobs:",
        len(relevant_jobs)
    )

    print(
        "Rejected jobs:",
        len(rejected_jobs)
    )


    if len(jobs) > 0:

        percentage = (
            len(relevant_jobs)
            / len(jobs)
        ) * 100

        print(
            f"Relevance rate: {percentage:.1f}%"
        )


    print("\n" + "=" * 70)
    print("REAL JOB FILTER TEST COMPLETED")
    print("=" * 70)


finally:

    db.close()