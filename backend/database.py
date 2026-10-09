from pathlib import Path

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, Profile, Job, Application, ActionLog


# ============================================================
# DATABASE PATH
# ============================================================

# Project root:
# AI resume project/

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATABASE_PATH = PROJECT_ROOT / "job_hunter.db"

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# ============================================================
# DATABASE ENGINE
# ============================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
    future=True
)


# ============================================================
# SESSION
# ============================================================

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# ============================================================
# CREATE DATABASE TABLES
# ============================================================

def init_db():
    """
    Create all database tables if they do not already exist.
    """

    Base.metadata.create_all(bind=engine)


# ============================================================
# DATABASE SESSION
# ============================================================

def get_db():
    """
    Create a database session.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# ============================================================
# GET PROFILE
# ============================================================

def get_profile(db: Session):
    """
    Get the first saved user profile.
    """

    statement = select(Profile).limit(1)

    return db.execute(statement).scalar_one_or_none()


# ============================================================
# GET JOB BY EXTERNAL ID
# ============================================================

def get_job_by_external_id(
    db: Session,
    external_id: str
):
    """
    Find a job using the ID provided by
    Adzuna or Remotive.
    """

    statement = select(Job).where(
        Job.external_id == external_id
    )

    return db.execute(statement).scalar_one_or_none()


# ============================================================
# GET JOB BY DATABASE ID
# ============================================================

def get_job(
    db: Session,
    job_id: int
):
    """
    Find a job using our internal database ID.
    """

    statement = select(Job).where(
        Job.id == job_id
    )

    return db.execute(statement).scalar_one_or_none()


# ============================================================
# CHECK IF ALREADY APPLIED
# ============================================================

def already_applied(
    db: Session,
    job_id: int
) -> bool:
    """
    Prevent the agent from applying
    to the same job twice.
    """

    statement = select(Application).where(
        Application.job_id == job_id
    )

    application = db.execute(
        statement
    ).scalar_one_or_none()

    return application is not None


# ============================================================
# LOG AGENT ACTION
# ============================================================

def log_action(
    db: Session,
    action: str,
    job_id: int | None = None,
    details: str = "",
    success: bool = True
):
    """
    Save every important agent action.
    """

    log = ActionLog(
        action=action,
        job_id=job_id,
        details=details,
        success=success
    )

    db.add(log)
    db.commit()

    return log


# ============================================================
# ADD JOB
# ============================================================

def add_job(
    db: Session,
    job: Job
):
    """
    Add a new job to the database.

    Returns:
        Job object if inserted.
        Existing job if duplicate.
    """

    existing_job = get_job_by_external_id(
        db,
        job.external_id
    )

    if existing_job:
        return existing_job

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


# ============================================================
# CREATE PROFILE
# ============================================================

def create_or_update_profile(
    db: Session,
    name: str = "",
    email: str = "",
    phone: str = "",
    location: str = "",
    roles: str = "",
    skills: str = "",
    minimum_salary: float = 0.0,
    remote_only: bool = False,
    resume_path: str = "",
    resume_text: str = ""
):
    """
    Create the user's career profile.

    If a profile already exists,
    update that profile instead.
    """

    profile = get_profile(db)

    if profile is None:

        profile = Profile(
            name=name,
            email=email,
            phone=phone,
            location=location,
            roles=roles,
            skills=skills,
            minimum_salary=minimum_salary,
            remote_only=remote_only,
            resume_path=resume_path,
            resume_text=resume_text
        )

        db.add(profile)

    else:

        profile.name = name
        profile.email = email
        profile.phone = phone
        profile.location = location
        profile.roles = roles
        profile.skills = skills
        profile.minimum_salary = minimum_salary
        profile.remote_only = remote_only
        profile.resume_path = resume_path
        profile.resume_text = resume_text

    db.commit()
    db.refresh(profile)

    return profile

