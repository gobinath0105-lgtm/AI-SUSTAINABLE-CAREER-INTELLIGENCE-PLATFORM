from backend.database import SessionLocal, init_db
from agent.matcher import is_relevant_job
from agent.ai_matcher import analyze_job


print("=" * 70)
print("AI JOB HUNTER - FILTERED JOB ANALYSIS")
print("=" * 70)


# ============================================================
# DATABASE
# ============================================================

init_db()

db = SessionLocal()


try:

    # --------------------------------------------------------
    # Get profile
    # --------------------------------------------------------

    profile = db.query(__import__(
        "backend.models",
        fromlist=["Profile"]
    ).Profile).first()

    if not profile:
        print("No profile found in database.")
        exit()

    resume_text = profile.resume_text or ""

    print()
    print(f"Resume: {profile.name}")
    print(f"Resume characters: {len(resume_text)}")

    # --------------------------------------------------------
    # Get jobs
    # --------------------------------------------------------

    Job = __import__(
        "backend.models",
        fromlist=["Job"]
    ).Job

    jobs = (
        db.query(Job)
        .order_by(Job.discovered_at.desc())
        .all()
    )

    print(f"Jobs in database: {len(jobs)}")


    # ========================================================
    # STEP 1: LOCAL RELEVANCE FILTER
    # ========================================================

    print()
    print("=" * 70)
    print("STEP 1: LOCAL RELEVANCE FILTER")
    print("=" * 70)

    relevant_jobs = []

    for job in jobs:

        result = is_relevant_job(
    resume_text,
    job.title or "",
    job.description or ""
        )

        if result["relevant"]:

            print()
            print(f"✓ {job.title}")
            print(f"  Relevance: {result.get('relevance_score', 'N/A')}")
            print(f"  Reason: {result.get('reason', 'No reason provided')}")

            relevant_jobs.append(
                (job, result)
            )

        else:

            print()
            print(f"✗ {job.title}")
            print("  Filtered out")

    print()
    print("-" * 70)

    print(f"Total jobs: {len(jobs)}")
    print(f"Relevant jobs: {len(relevant_jobs)}")


    # ========================================================
    # STEP 2: GEMINI AI ANALYSIS
    # ========================================================

    print()
    print("=" * 70)
    print("STEP 2: GEMINI AI ANALYSIS")
    print("=" * 70)

    ai_results = []
    ai_failures = []

    for index, (job, local_result) in enumerate(
        relevant_jobs,
        start=1
    ):

        print()
        print(
            f"[{index}/{len(relevant_jobs)}] "
            f"{job.title}"
        )

        print(f"Company: {job.company}")
        print("Sending to Gemini...")

        result = analyze_job(
            resume_text=resume_text,
            job_title=job.title or "",
            job_description=job.description or "",
            job_company=job.company or ""
        )

        # ----------------------------------------------------
        # AI ERROR
        # ----------------------------------------------------

        if not result.get("success", False):

            print("Gemini analysis failed.")

            print(
                f"Error: {result.get('error', 'Unknown error')}"
            )

            ai_failures.append(
                {
                    "job": job,
                    "result": result
                }
            )

            continue

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        print(
            f"AI Match Score: "
            f"{result.get('score')}"
        )

        print(
            f"Recommendation: "
            f"{result.get('recommendation')}"
        )

        result["job"] = job
        result["local_relevance"] = local_result

        ai_results.append(result)


    # ========================================================
    # STEP 3: SORT AI RESULTS
    # ========================================================

    ai_results.sort(
        key=lambda x: x.get("score", 0),
        reverse=True
    )


    # ========================================================
    # FINAL RANKING
    # ========================================================

    print()
    print("=" * 70)
    print("🔥 FINAL AI JOB RANKING")
    print("=" * 70)

    if not ai_results:

        print()
        print("No jobs were successfully analyzed by Gemini.")

    else:

        for rank, result in enumerate(
            ai_results,
            start=1
        ):

            job = result["job"]

            print()
            print("-" * 70)

            print(f"#{rank} {job.title}")
            print(f"Company: {job.company}")
            print(f"Source: {job.source}")

            print(
                f"AI Match Score: "
                f"{result.get('score')} /100"
            )

            print(
                f"Recommendation: "
                f"{result.get('recommendation')}"
            )

            print()
            print("Reason:")
            print(result.get("reason", "N/A"))

            print()
            print("Strengths:")

            for strength in result.get(
                "strengths",
                []
            ):

                print(f"  ✓ {strength}")

            print()
            print("Missing Skills:")

            for skill in result.get(
                "missing_skills",
                []
            ):

                print(f"  ✗ {skill}")

            print()
            print(f"URL: {job.job_url}")


    # ========================================================
    # SUMMARY
    # ========================================================

    print()
    print("=" * 70)
    print("JOB HUNTER ANALYSIS COMPLETED")
    print("=" * 70)

    print()
    print(f"Jobs collected: {len(jobs)}")
    print(
        f"Jobs passed local filter: "
        f"{len(relevant_jobs)}"
    )

    print(
        f"Jobs analyzed successfully by Gemini: "
        f"{len(ai_results)}"
    )

    print(
        f"Gemini analysis failures: "
        f"{len(ai_failures)}"
    )

finally:

    db.close()