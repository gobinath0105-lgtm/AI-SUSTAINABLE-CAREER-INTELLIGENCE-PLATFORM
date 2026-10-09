from agent.matcher import match_job


# ============================================================
# SAMPLE RESUME
# ============================================================

resume_text = """
B.Tech Artificial Intelligence and Data Science student.

Skills:
Python, SQL, Machine Learning, Deep Learning,
TensorFlow, Keras, NLP, Transformers, LLM,
RAG, Vector Database, Git, Streamlit.

Projects:
House Price Prediction using Machine Learning.
Customer Churn Prediction using Logistic Regression.
MNIST Image Classification using CNN.
Cat vs Dog Image Classification using Deep Learning.
"""


# ============================================================
# SAMPLE JOB
# ============================================================

job_title = "AI Engineer"

job_company = "Example AI Company"

job_description = """
We are looking for an AI Engineer with experience in
Python, Machine Learning, Deep Learning, NLP,
LLMs, RAG, FastAPI, Docker and Git.

The candidate should be able to build and deploy
AI applications and work with modern generative AI systems.
"""


# ============================================================
# RUN MATCHING
# ============================================================

print("Sending job to Claude...")
print()

result = match_job(
    resume_text=resume_text,
    job_title=job_title,
    job_description=job_description,
    job_company=job_company
)


# ============================================================
# DISPLAY RESULT
# ============================================================

print("=" * 60)
print("AI JOB MATCH RESULT")
print("=" * 60)

print(
    f"Match Score: {result['score']}/100"
)

print()

print(
    "Reason:"
)

print(
    result["reason"]
)

print()

print(
    "Missing Skills:"
)

if result["missing_skills"]:

    for skill in result["missing_skills"]:
        print(
            f"- {skill}"
        )

else:

    print(
        "No major missing skills identified."
    )

print("=" * 60)