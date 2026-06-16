from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.extensions import db


class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'

    id = db.Column(db.String(36), primary_key=True, default=lambda: uuid4().hex)
    session_id = db.Column(
        db.String(36),
        db.ForeignKey('chat_sessions.id', ondelete='CASCADE'),
        nullable=False,
        index=True,
    )
    role = db.Column(db.String(20), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tokens_in = db.Column(db.Integer, default=0, nullable=False)
    tokens_out = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    session = db.relationship('ChatSession', back_populates='messages')
