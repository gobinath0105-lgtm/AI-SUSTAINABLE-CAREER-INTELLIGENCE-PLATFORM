# 🚀 AI Sustainable Career Intelligence Platform

An AI-powered career intelligence platform that analyzes resumes, evaluates job compatibility, identifies skill gaps, and helps students discover suitable career opportunities. The project also includes an AI Job Hunter module that uses real job sources and Gemini AI to evaluate job relevance.

## 🎯 Problem Statement

Students and early-career candidates often struggle to identify suitable job opportunities, understand the skills employers expect, and determine what they should learn next.

Traditional job portals primarily list vacancies. Candidates still need to manually compare job requirements with their resumes and identify missing skills.

## 💡 Our Solution

The AI Sustainable Career Intelligence Platform combines resume analysis, job matching, skill-gap analysis, and AI-powered job evaluation in one application.

The goal is to help candidates make more informed career decisions and focus their learning on relevant opportunities.

## ✨ Key Features

### Career Intelligence Platform

* **Resume Analysis:** Extracts and analyzes resume information.
* **ATS Score:** Evaluates resume alignment with job-related criteria.
* **Skill Intelligence:** Identifies technical skills and areas for improvement.
* **Job Matching:** Compares candidate skills with job requirements.
* **Skill Gap Analysis:** Highlights skills that may need improvement.
* **Career Recommendations:** Helps users explore suitable career paths.
* **What-If Simulation:** Supports exploration of how additional skills may affect job matching.
* **Project Recommendations:** Suggests projects relevant to career goals.
* **AI Career Advisor:** Provides career guidance.
* **Interview Readiness:** Supports interview preparation.

### 🤖 AI Job Hunter Agent

* **Real Job Sources:** Integrates with the Remotive API and supports Adzuna API integration.
* **Job Database:** Stores discovered job information using SQLite and SQLAlchemy.
* **Local Relevance Filter:** Filters out jobs that appear unrelated to the candidate's AI and Data Science career goals.
* **Gemini AI Job Analysis:** Evaluates resume-to-job compatibility.
* **Match Scoring:** Produces a job match score and recommendation.
* **Explainable Results:** Shows matching strengths, missing skills, and the reasons behind recommendations.
* **Job Ranking:** Ranks analyzed vacancies to help prioritize opportunities.
* **Duplicate Prevention Foundation:** Includes database support for identifying previously stored jobs and tracking application records.

## 🧠 Technology Stack

| Area                  | Technologies                         |
| --------------------- | ------------------------------------ |
| Frontend              | Streamlit                            |
| Programming Language  | Python                               |
| Data Processing       | Pandas                               |
| Resume PDF Processing | pypdf                                |
| Machine Learning      | Scikit-learn                         |
| Generative AI         | Google Gemini API                    |
| Job Data              | Remotive API, Adzuna API integration |
| Database              | SQLite                               |
| ORM                   | SQLAlchemy                           |
| Configuration         | python-dotenv                        |

## ⚙️ Project Workflow

1. The user uploads a resume or uses a saved resume profile.
2. The platform extracts relevant skills and career information.
3. The job discovery module retrieves vacancies from supported job sources.
4. A rule-based filter removes clearly irrelevant job listings.
5. Gemini AI evaluates the remaining jobs against the candidate's resume.
6. The system returns match scores, recommendations, strengths, missing skills, and explanations.
7. Jobs are ranked to help the candidate prioritize opportunities.

## 🏗️ AI Job Hunter Architecture

```text
Resume / Candidate Profile
          |
          v
Job Discovery APIs
          |
          v
SQLite Job Database
          |
          v
Rule-Based Relevance Filter
          |
          v
Gemini AI Resume-to-Job Analysis
          |
          v
Match Score + Skill Gaps + Explanation
          |
          v
Ranked Job Recommendations
```

The system uses a **hybrid AI approach**: rule-based logic performs the initial filtering, while Gemini provides generative AI analysis and explanations.

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```text
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite

REMOTIVE_ENABLED=true

ADZUNA_APP_ID=
ADZUNA_APP_KEY=
ADZUNA_COUNTRY=in

DEFAULT_LOCATION=India
DEFAULT_MIN_SALARY=0
DEFAULT_REMOTE_ONLY=false
```

Use your own API credentials. Adzuna integration requires valid credentials. Check the current Gemini model availability before running the application.

**Security:** Never commit `.env`, API keys, passwords, personal resume files, or your local database to a public repository.

### 5. Run the Streamlit application

```bash
streamlit run app.py
```

## 📂 Project Structure

```text
AI resume project/
├── app.py
├── ats_engine.py
├── nlp_engine.py
├── job_agent.py
├── jobs.csv
├── skill_impact.csv
├── projects.csv
├── requirements.txt
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── application_agent.py
│   ├── ai_matcher.py
│   ├── job_sources.py
│   ├── matcher.py
│   ├── notifications.py
│   └── resume_tailor.py
├── backend/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── scheduler.py
├── data/
│   ├── resumes/
│   └── tailored/
└── .streamlit/
    └── secrets.toml
```

Some modules are part of the planned or ongoing development workflow. Their presence in the project structure does not mean every feature is fully implemented.

## 🔬 Current Development Status

* [x] Resume and career intelligence features
* [x] Job source integration
* [x] SQLite database setup
* [x] Rule-based job relevance filtering
* [x] Gemini AI job analysis
* [x] Match scoring and job ranking
* [ ] Telegram-based application approval
* [ ] Automated resume tailoring and cover letters
* [ ] Browser-based application submission
* [ ] Complete application tracking and scheduled follow-ups

Automated applications are not yet a complete end-to-end workflow. Website-specific forms, authentication, and CAPTCHA challenges may require manual action.

## 🔮 Future Enhancements

* Telegram notifications and approval workflow
* Resume tailoring for individual vacancies
* AI-generated cover letters grounded in the candidate's actual experience
* Application tracking dashboard
* Scheduled job discovery and follow-up reminders
* Improved matching evaluation using labeled test data
* More job-source integrations

## 👨‍💻 Author

**Gobinath**
B.Tech Artificial Intelligence and Data Science

* LinkedIn: https://www.linkedin.com/in/gobinath-gobi
* GitHub: https://github.com/gobinath0105-lgtm

## 📄 Disclaimer

This project is developed for educational and career-support purposes. Match scores are estimates, not guarantees of selection or employment. Candidates should review job requirements and application details before submitting applications.
