from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.extensions import db


class JobPosting(db.Model):
    __tablename__ = 'job_postings'

    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid4().hex)
    title = db.Column(db.String(255), nullable=False)
    team = db.Column(db.String(100), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    employment_type = db.Column('type', db.String(100), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    responsibilities = db.Column(db.JSON, nullable=True)
    requirements = db.Column(db.JSON, nullable=True)
    status = db.Column(db.String(20), default='active', nullable=False, index=True)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
