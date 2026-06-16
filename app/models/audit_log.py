from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.extensions import db


class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id            = db.Column(db.String(36), primary_key=True, default=lambda: uuid4().hex)
    actor_user_id = db.Column(db.String(36), db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    action        = db.Column(db.String(100), nullable=False, index=True)
    entity        = db.Column(db.String(100), nullable=False, index=True)
    entity_id     = db.Column(db.String(36),  nullable=True,  index=True)
    diff          = db.Column(db.JSON,        nullable=True)
    ip            = db.Column(db.String(64),  nullable=True)
    request_id    = db.Column(db.String(64),  nullable=True)
    created_at    = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
