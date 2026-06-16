from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from app.extensions import db


class PageView(db.Model):
    __tablename__ = 'page_views'

    id          = db.Column(db.String(36), primary_key=True, default=lambda: uuid4().hex)
    path        = db.Column(db.String(1024), nullable=False, index=True)
    referrer    = db.Column(db.String(1024), nullable=True)
    device_type = db.Column(db.String(20),   nullable=True)   # desktop | mobile | tablet
    browser     = db.Column(db.String(50),   nullable=True)
    os          = db.Column(db.String(50),   nullable=True)
    session_id  = db.Column(db.String(64),   nullable=True, index=True)
    ip_hash     = db.Column(db.String(64),   nullable=True)
    created_at  = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
