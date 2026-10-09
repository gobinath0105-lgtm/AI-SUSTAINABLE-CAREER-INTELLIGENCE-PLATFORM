import os
import json
import time

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT
# ============================================================

load_dotenv()


GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.5-flash-lite"
)


# ============================================================
# GEMINI CLIENT
# ============================================================

client = None

if GEMINI_API_KEY:

    client = genai.Client(
        api_key=GEMINI_API_KEY
    )


# ============================================================
# AI JOB ANALYSIS
# ============================================================

def analyze_job(
    resume_text,
    job_title,
    job_description,
    job_company=""
):

    if not client:

        print(
            "Gemini API key not configured."
        )

        return {
            "success": False,
            "score": None,
            "recommendation": "AI_ERROR",
            "reason": "Gemini API key is not configured.",
            "strengths": [],
            "missing_skills": [],
            "error": "API key missing"
        }


    # ========================================================
    # PROMPT
    # ========================================================

    prompt = f"""
You are an AI job matching assistant.

Analyze the candidate's resume against the job.

IMPORTANT RULES:

1. Never invent skills.
2. Never invent experience.
3. Never assume the candidate has professional experience
   unless the resume clearly says so.
4. Give a realistic match score from 0 to 100.
5. Consider job title, required skills, experience,
   education, and responsibilities.
6. A senior role should receive a low score if the candidate
   does not have the required professional experience.
7. Return ONLY valid JSON.

CANDIDATE RESUME:

{resume_text}


JOB TITLE:

{job_title}


COMPANY:

{job_company}


JOB DESCRIPTION:

{job_description}


Return exactly this JSON structure:

{{
    "score": 0,
    "recommendation": "Apply",
    "reason": "Short explanation",
    "strengths": [
        "strength 1",
        "strength 2"
    ],
    "missing_skills": [
        "missing skill 1",
        "missing skill 2"
    ]
}}

The recommendation must be either:

"Apply"

or

"Skip"
"""


    # ========================================================
    # RETRY CONFIGURATION
    # ========================================================

    max_retries = 3

    retry_delays = [
        5,
        10,
        20
    ]


    # ========================================================
    # GEMINI REQUEST
    # ========================================================

    for attempt in range(
        max_retries
    ):

        try:

            print(
                f"Gemini attempt "
                f"{attempt + 1}/{max_retries}..."
            )

            response = client.models.generate_content(

                model=GEMINI_MODEL,

                contents=prompt
            )


            # ------------------------------------------------
            # GET RESPONSE TEXT
            # ------------------------------------------------

            response_text = (
                response.text
                if response.text
                else ""
            )


            response_text = response_text.strip()


            # ------------------------------------------------
            # REMOVE MARKDOWN CODE FENCES
            # ------------------------------------------------

            if response_text.startswith(
                "```"
            ):

                response_text = (
                    response_text
                    .replace(
                        "```json",
                        ""
                    )
                    .replace(
                        "```",
                        ""
                    )
                    .strip()
                )


            # ------------------------------------------------
            # PARSE JSON
            # ------------------------------------------------

            result = json.loads(
                response_text
            )


            # ------------------------------------------------
            # VALIDATE SCORE
            # ------------------------------------------------

            score = result.get(
                "score",
                0
            )

            try:

                score = float(score)

            except:

                score = 0


            score = max(
                0,
                min(
                    100,
                    score
                )
            )


            # ------------------------------------------------
            # VALIDATE RECOMMENDATION
            # ------------------------------------------------

            recommendation = result.get(
                "recommendation",
                "Skip"
            )


            if recommendation not in [
                "Apply",
                "Skip"
            ]:

                recommendation = "Skip"


            # ------------------------------------------------
            # VALIDATE LISTS
            # ------------------------------------------------

            strengths = result.get(
                "strengths",
                []
            )

            missing_skills = result.get(
                "missing_skills",
                []
            )


            if not isinstance(
                strengths,
                list
            ):

                strengths = []


            if not isinstance(
                missing_skills,
                list
            ):

                missing_skills = []


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            print(
                "Gemini response received."
            )


            return {

                "success": True,

                "score": score,

                "recommendation":
                    recommendation,

                "reason":
                    result.get(
                        "reason",
                        ""
                    ),

                "strengths":
                    strengths,

                "missing_skills":
                    missing_skills,

                "error":
                    None
            }


        # ====================================================
        # TEMPORARY GEMINI ERROR
        # ====================================================

        except Exception as e:

            error_text = str(e)

            print(
                "\nGemini error:"
            )

            print(
                error_text
            )


            # ------------------------------------------------
            # RETRY 503 / TEMPORARY ERRORS
            # ------------------------------------------------

            is_temporary = (
                "503" in error_text
                or
                "UNAVAILABLE" in error_text
                or
                "429" in error_text
                or
                "RESOURCE_EXHAUSTED" in error_text
            )


            if (
                is_temporary
                and attempt < max_retries - 1
            ):

                delay = retry_delays[
                    attempt
                ]

                print(
                    f"\nTemporary Gemini error."
                )

                print(
                    f"Retrying in {delay} seconds..."
                )

                time.sleep(
                    delay
                )

                continue


            # ------------------------------------------------
            # FINAL FAILURE
            # ------------------------------------------------

            print(
                "\nGemini analysis failed "
                "after all attempts."
            )


            return {

                "success": False,

                "score": None,

                "recommendation":
                    "AI_ERROR",

                "reason":
                    "Gemini AI analysis failed temporarily.",

                "strengths": [],

                "missing_skills": [],

                "error":
                    error_text
            }


    # ========================================================
    # SAFETY FALLBACK
    # ========================================================

    return {

        "success": False,

        "score": None,

        "recommendation":
            "AI_ERROR",

        "reason":
            "Gemini analysis could not be completed.",

        "strengths": [],

        "missing_skills": [],

        "error":
            "Unknown Gemini error"
    }


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("GEMINI AI MATCHER TEST")
    print("=" * 60)

    test_resume = """
    B.Tech Artificial Intelligence and Data Science student.

    Skills:
    Python, SQL, Machine Learning,
    Deep Learning, TensorFlow, NLP, RAG.
    """

    test_job = """
    AI Engineer Intern

    Looking for Python, Machine Learning,
    NLP and TensorFlow skills.
    """

    result = analyze_job(

        resume_text=test_resume,

        job_title="AI Engineer Intern",

        job_description=test_job,

        job_company="Test Company"
    )


    print("\nResult:")
    print(
        json.dumps(
            result,
            indent=4
        )
    )