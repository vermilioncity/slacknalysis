"""create members table

Revision ID: af83a7904c99
Revises: 
Create Date: 2019-10-26 20:42:40.428762+00:00

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af83a7904c99'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.String(15), primary_key=True),
        sa.Column('user_name', sa.String(30), nullable=False, unique=True),
    )


def downgrade():
    op.drop_table('users')
