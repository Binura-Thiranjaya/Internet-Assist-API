"""add page_views table

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-06-11 00:00:00.000002

"""
from alembic import op
import sqlalchemy as sa

revision = 'c3d4e5f6a7b8'
down_revision = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('page_views',
        sa.Column('id',          sa.String(36),            nullable=False),
        sa.Column('path',        sa.String(1024),          nullable=False),
        sa.Column('referrer',    sa.String(1024),          nullable=True),
        sa.Column('device_type', sa.String(20),            nullable=True),
        sa.Column('browser',     sa.String(50),            nullable=True),
        sa.Column('os',          sa.String(50),            nullable=True),
        sa.Column('session_id',  sa.String(64),            nullable=True),
        sa.Column('ip_hash',     sa.String(64),            nullable=True),
        sa.Column('created_at',  sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_page_views_path',       'page_views', ['path'],       unique=False)
    op.create_index('ix_page_views_session_id', 'page_views', ['session_id'], unique=False)
    op.create_index('ix_page_views_created_at', 'page_views', ['created_at'], unique=False)


def downgrade():
    op.drop_index('ix_page_views_created_at', table_name='page_views')
    op.drop_index('ix_page_views_session_id',  table_name='page_views')
    op.drop_index('ix_page_views_path',        table_name='page_views')
    op.drop_table('page_views')
