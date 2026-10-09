import os

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.7-flash"
).strip()


# ============================================================
# CHECK API KEY
# ============================================================

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing from .env"
    )


# ============================================================
# CREATE GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# TEST AI
# ============================================================

print()
print("=" * 60)
print("GEMINI AI TEST")
print("=" * 60)

print(f"Model: {GEMINI_MODEL}")
print()
print("Sending request to Gemini...")


response = client.models.generate_content(
    model=GEMINI_MODEL,
    contents="""
You are an AI career assistant.

A student knows:
Python, Machine Learning, Deep Learning, NLP and RAG.

They want to become an AI Engineer.

Give:
1. Their strongest skills
2. Three missing skills
3. One short recommendation

Use simple English.
"""
)


# ============================================================
# DISPLAY RESPONSE
# ============================================================

print()
print("Gemini response:")
print("-" * 60)
print(response.text)
print("-" * 60)

print()
print("Gemini AI is working successfully!")
print("=" * 60)