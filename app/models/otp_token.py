from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.extensions import db


class OtpToken(db.Model):
    __tablename__ = 'otp_tokens'

    id           = db.Column(db.String(36), primary_key=True, default=lambda: uuid4().hex)
    user_id      = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    session_hash = db.Column(db.String(64), nullable=False, unique=True, index=True)
    otp_hash     = db.Column(db.String(64), nullable=False)
    expires_at   = db.Column(db.DateTime(timezone=True), nullable=False)
    attempts     = db.Column(db.Integer, default=0, nullable=False)
    created_at   = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
