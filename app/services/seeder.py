from __future__ import annotations

from flask import current_app

from app.extensions import db
from app.logging import logger
from app.models.role import Role
from app.models.user import User

SEED_ROLES = ['admin', 'staff']


def _seed_roles() -> None:
    added = []
    for name in SEED_ROLES:
        if not Role.query.filter_by(name=name).first():
            db.session.add(Role(name=name))
            added.append(name)
    db.session.flush()
    if added:
        logger.info('roles_seeded', roles=added)
    else:
        logger.info('roles_already_exist')


def _seed_admin_user() -> None:
    email = current_app.config['INITIAL_ADMIN_EMAIL'].lower()
    password = current_app.config['INITIAL_ADMIN_PASSWORD']

    if User.query.filter_by(email=email).first():
        logger.info('admin_user_already_exists', email=email)
        return

    admin_role = Role.query.filter_by(name='admin').first()
    if not admin_role:
        raise RuntimeError('admin role missing — ensure _seed_roles ran first')

    user = User(email=email, full_name='Internet Assist Admin')
    user.set_password(password)
    user.roles.append(admin_role)
    db.session.add(user)
    db.session.commit()
    logger.info('admin_user_created', email=email)


def run_seed() -> None:
    db.create_all()
    _seed_roles()
    _seed_admin_user()
    logger.info('seed_complete')
