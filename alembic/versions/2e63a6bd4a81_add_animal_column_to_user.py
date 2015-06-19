"""Add animal column to user

Revision ID: 2e63a6bd4a81
Revises: 
Create Date: 2015-06-12 21:19:16.029619

"""

# revision identifiers, used by Alembic.
revision = '2e63a6bd4a81'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('User', sa.Column('animal', sa.String(60)))


def downgrade():
    p.drop_column('User', sa.Column('animal'))
