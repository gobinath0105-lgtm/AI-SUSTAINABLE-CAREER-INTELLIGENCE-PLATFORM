from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# ============================================================
# BASE
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# JOB STATUS
# ============================================================

class JobStatus(str, Enum):
    FOUND = "Found"
    APPROVED = "Approved"
    APPLIED = "Applied"
    INTERVIEW = "Interview"
    REJECTED = "Rejected"
    OFFER = "Offer"
    FAILED = "Failed"


# ============================================================
# PROFILE
# ============================================================

class Profile(Base):
    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(150),
        default=""
    )

    email: Mapped[str] = mapped_column(
        String(200),
        default=""
    )

    phone: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    location: Mapped[str] = mapped_column(
        String(150),
        default=""
    )

    roles: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    skills: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    minimum_salary: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    remote_only: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    resume_path: Mapped[str] = mapped_column(
        String(500),
        default=""
    )

    resume_text: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


# ============================================================
# JOB
# ============================================================

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Unique ID from Adzuna / Remotive
    external_id: Mapped[str] = mapped_column(
        String(300),
        unique=True,
        index=True
    )

    source: Mapped[str] = mapped_column(
        String(50),
        default=""
    )

    title: Mapped[str] = mapped_column(
        String(300),
        default=""
    )

    company: Mapped[str] = mapped_column(
        String(300),
        default=""
    )

    location: Mapped[str] = mapped_column(
        String(300),
        default=""
    )

    description: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    job_url: Mapped[str] = mapped_column(
        String(1000),
        default=""
    )

    salary_min: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    salary_max: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    remote: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    published_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    discovered_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    # Claude matching result
    match_score: Mapped[float] = mapped_column(
        Float,
        default=0.0
    )

    match_reason: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    missing_skills: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default=JobStatus.FOUND.value
    )

    approved_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    applied_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationship with Application
    application: Mapped["Application | None"] = relationship(
        "Application",
        back_populates="job",
        uselist=False
    )


# ============================================================
# APPLICATION
# ============================================================

class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    job_id: Mapped[int] = mapped_column(
        ForeignKey("jobs.id"),
        unique=True,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default=JobStatus.FOUND.value
    )

    tailored_resume_path: Mapped[str] = mapped_column(
        String(500),
        default=""
    )

    cover_letter: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    error_message: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    applied_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    follow_up_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    response_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationship with Job
    job: Mapped["Job"] = relationship(
        "Job",
        back_populates="application"
    )


# ============================================================
# ACTION LOG
# ============================================================

class ActionLog(Base):
    __tablename__ = "action_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    action: Mapped[str] = mapped_column(
        String(100)
    )

    job_id: Mapped[int | None] = mapped_column(
        ForeignKey("jobs.id"),
        nullable=True
    )

    details: Mapped[str] = mapped_column(
        Text,
        default=""
    )

    success: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    