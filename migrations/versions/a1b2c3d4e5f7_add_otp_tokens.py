"""add otp_tokens table

Revision ID: a1b2c3d4e5f7
Revises: d5fe4d490110
Create Date: 2026-06-11 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f7'
down_revision = 'd5fe4d490110'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('otp_tokens',
        sa.Column('id',           sa.String(36), nullable=False),
        sa.Column('user_id',      sa.String(36), nullable=False),
        sa.Column('session_hash', sa.String(64), nullable=False),
        sa.Column('otp_hash',     sa.String(64), nullable=False),
        sa.Column('expires_at',   sa.DateTime(timezone=True), nullable=False),
        sa.Column('attempts',     sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at',   sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_otp_tokens_session_hash', 'otp_tokens', ['session_hash'], unique=True)
    op.create_index('ix_otp_tokens_user_id',      'otp_tokens', ['user_id'],      unique=False)


def downgrade():
    op.drop_index('ix_otp_tokens_session_hash', table_name='otp_tokens')
    op.drop_index('ix_otp_tokens_user_id',      table_name='otp_tokens')
    op.drop_table('otp_tokens')
