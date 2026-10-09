import os
from datetime import datetime

import httpx
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()


ADZUNA_APP_ID = os.getenv("ADZUNA_APP_ID", "")
ADZUNA_APP_KEY = os.getenv("ADZUNA_APP_KEY", "")
ADZUNA_COUNTRY = os.getenv("ADZUNA_COUNTRY", "in")

REMOTIVE_ENABLED = os.getenv(
    "REMOTIVE_ENABLED",
    "true"
).lower() == "true"


# ============================================================
# REMOTIVE
# ============================================================

def fetch_remotive_jobs(
    search: str = "python",
    limit: int = 20
):
    """
    Fetch remote jobs from Remotive.

    Returns a list of normalized job dictionaries.
    """

    if not REMOTIVE_ENABLED:
        return []

    url = "https://remotive.com/api/remote-jobs"

    params = {
        "search": search
    }

    try:

        response = httpx.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        jobs = data.get("jobs", [])

        normalized_jobs = []

        for job in jobs[:limit]:

            normalized_jobs.append(
                {
                    "external_id": f"remotive-{job.get('id')}",

                    "source": "Remotive",

                    "title": job.get(
                        "title",
                        ""
                    ),

                    "company": job.get(
                        "company_name",
                        ""
                    ),

                    "location": job.get(
                        "candidate_required_location",
                        "Remote"
                    ),

                    "description": job.get(
                        "description",
                        ""
                    ),

                    "job_url": job.get(
                        "url",
                        ""
                    ),

                    "salary_min": 0.0,

                    "salary_max": 0.0,

                    "remote": True,

                    "published_at": parse_date(
                        job.get("publication_date")
                    )
                }
            )

        return normalized_jobs

    except httpx.HTTPError as error:

        print(
            f"Remotive API error: {error}"
        )

        return []

    except Exception as error:

        print(
            f"Unexpected Remotive error: {error}"
        )

        return []


# ============================================================
# ADZUNA
# ============================================================

def fetch_adzuna_jobs(
    search: str = "python",
    location: str = "India",
    results_per_page: int = 20
):
    """
    Fetch jobs from Adzuna.

    If API credentials are not configured,
    this function safely returns an empty list.
    """

    if not ADZUNA_APP_ID or not ADZUNA_APP_KEY:

        print(
            "Adzuna credentials not configured."
        )

        return []

    url = (
        f"https://api.adzuna.com/v1/api/jobs/"
        f"{ADZUNA_COUNTRY}/search/1"
    )

    params = {
        "app_id": ADZUNA_APP_ID,
        "app_key": ADZUNA_APP_KEY,
        "results_per_page": results_per_page,
        "what": search,
        "where": location,
        "content-type": "application/json"
    }

    try:

        response = httpx.get(
            url,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        jobs = data.get(
            "results",
            []
        )

        normalized_jobs = []

        for job in jobs:

            normalized_jobs.append(
                {
                    "external_id": (
                        f"adzuna-{job.get('id')}"
                    ),

                    "source": "Adzuna",

                    "title": job.get(
                        "title",
                        ""
                    ),

                    "company": (
                        job.get("company", {})
                        .get("display_name", "")
                    ),

                    "location": (
                        job.get("location", {})
                        .get("display_name", "")
                    ),

                    "description": job.get(
                        "description",
                        ""
                    ),

                    "job_url": job.get(
                        "redirect_url",
                        ""
                    ),

                    "salary_min": float(
                        job.get(
                            "salary_min",
                            0
                        ) or 0
                    ),

                    "salary_max": float(
                        job.get(
                            "salary_max",
                            0
                        ) or 0
                    ),

                    "remote": is_remote_job(
                        job
                    ),

                    "published_at": parse_date(
                        job.get("created")
                    )
                }
            )

        return normalized_jobs

    except httpx.HTTPError as error:

        print(
            f"Adzuna API error: {error}"
        )

        return []

    except Exception as error:

        print(
            f"Unexpected Adzuna error: {error}"
        )

        return []


# ============================================================
# REMOTE DETECTION
# ============================================================

def is_remote_job(job: dict) -> bool:

    text = " ".join(
        [
            str(job.get("title", "")),
            str(
                job.get(
                    "description",
                    ""
                )
            ),
            str(
                job.get(
                    "location",
                    {}
                )
            )
        ]
    ).lower()

    remote_words = [
        "remote",
        "work from home",
        "wfh"
    ]

    return any(
        word in text
        for word in remote_words
    )


# ============================================================
# DATE PARSER
# ============================================================

def parse_date(
    value
):
    """
    Convert an API date string into datetime.
    """

    if not value:
        return None

    try:

        value = value.replace(
            "Z",
            "+00:00"
        )

        return datetime.fromisoformat(
            value
        )

    except Exception:

        return None


# ============================================================
# COMBINED JOB SEARCH
# ============================================================

def search_jobs(
    search: str = "python",
    location: str = "India",
    limit: int = 20
):
    """
    Search all enabled job sources.
    """

    all_jobs = []

    # Remotive
    remotive_jobs = fetch_remotive_jobs(
        search=search,
        limit=limit
    )

    all_jobs.extend(
        remotive_jobs
    )

    # Adzuna
    adzuna_jobs = fetch_adzuna_jobs(
        search=search,
        location=location,
        results_per_page=limit
    )

    all_jobs.extend(
        adzuna_jobs
    )

    return all_jobs