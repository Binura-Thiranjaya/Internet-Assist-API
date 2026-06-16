from __future__ import annotations

from app.extensions import db
from app.logging import logger
from app.models.audit_log import AuditLog


def log_audit_action(
    *,
    actor_user_id=None,
    action: str,
    entity: str,
    entity_id: str | None = None,
    diff=None,
    ip: str | None = None,
    request_id: str | None = None,
) -> None:
    entry = AuditLog(
        actor_user_id=actor_user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        diff=diff,
        ip=ip,
        request_id=request_id,
    )
    db.session.add(entry)
    db.session.commit()
    logger.info('audit_logged', action=action, entity=entity, entity_id=entity_id)
