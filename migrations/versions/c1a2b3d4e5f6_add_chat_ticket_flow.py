"""add chat ticket flow fields

Revision ID: c1a2b3d4e5f6
Revises: 0d91efc0794c
Create Date: 2026-05-07 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c1a2b3d4e5f6'
down_revision = '0d91efc0794c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('chat_sessions', sa.Column('ticket_flow_state', sa.String(length=50), nullable=True))
    # JSON type may not be supported on all DBs; use sa.JSON where available
    try:
        op.add_column('chat_sessions', sa.Column('ticket_flow_data', sa.JSON(), nullable=True))
    except Exception:
        op.add_column('chat_sessions', sa.Column('ticket_flow_data', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('chat_sessions', 'ticket_flow_data')
    op.drop_column('chat_sessions', 'ticket_flow_state')
