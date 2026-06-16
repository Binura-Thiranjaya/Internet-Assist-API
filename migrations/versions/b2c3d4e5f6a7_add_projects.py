"""add projects table

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f7
Create Date: 2026-06-11 00:00:00.000001

"""
from alembic import op
import sqlalchemy as sa

revision = 'b2c3d4e5f6a7'
down_revision = 'a1b2c3d4e5f7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('projects',
        sa.Column('id',        sa.String(36), nullable=False),
        sa.Column('title',     sa.String(255), nullable=False),
        sa.Column('client',    sa.String(255), nullable=True),
        sa.Column('industry',  sa.String(100), nullable=True),
        sa.Column('summary',   sa.Text(), nullable=False),
        sa.Column('challenge', sa.Text(), nullable=True),
        sa.Column('solution',  sa.Text(), nullable=True),
        sa.Column('outcome',   sa.Text(), nullable=True),
        sa.Column('tags',      sa.JSON(), nullable=True),
        sa.Column('image_url', sa.String(1024), nullable=True),
        sa.Column('status',    sa.String(30), nullable=False, server_default='draft'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_projects_status', 'projects', ['status'], unique=False)


def downgrade():
    op.drop_index('ix_projects_status', table_name='projects')
    op.drop_table('projects')
