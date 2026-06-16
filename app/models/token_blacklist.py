from __future__ import annotations

from datetime import datetime, timezone

from app.extensions import db


class TokenBlacklist(db.Model):
    __tablename__ = 'token_blacklist'

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jti        = db.Column(db.String(36), nullable=False, unique=True, index=True)
    expires_at = db.Column(db.DateTime(timezone=True), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)

    @classmethod
    def is_revoked(cls, jti: str) -> bool:
        now = datetime.now(timezone.utc)
        entry = cls.query.filter_by(jti=jti).first()
        return entry is not None and entry.expires_at.replace(tzinfo=timezone.utc) > now

    @classmethod
    def purge_expired(cls) -> None:
        now = datetime.now(timezone.utc)
        cls.query.filter(cls.expires_at < now).delete()
        db.session.commit()
