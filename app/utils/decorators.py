from __future__ import annotations

from functools import wraps

from flask import abort, g
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.extensions import db
from app.models.user import User


def roles_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user = db.session.get(User, get_jwt_identity())
            if not user or not any(role.name in roles for role in user.roles):
                abort(403, description='Admin role required')
            g.current_user = user
            return fn(*args, **kwargs)

        return wrapper

    return decorator
