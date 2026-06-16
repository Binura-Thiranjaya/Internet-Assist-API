"""merge ticket and chat branches

Revision ID: f2147878404f
Revises: 12860312c804, c1a2b3d4e5f6
Create Date: 2026-05-07 19:32:52.674312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f2147878404f'
down_revision = ('12860312c804', 'c1a2b3d4e5f6')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
