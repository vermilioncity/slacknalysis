"""add reaction table

Revision ID: e40505630c39
Revises: 0465ca966d2f
Create Date: 2019-10-27 06:15:31.038044+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e40505630c39'
down_revision = '0465ca966d2f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'reactions',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('message_ts', sa.Numeric(16, 6), sa.ForeignKey('messages.ts'), nullable=False),
        sa.Column('name', sa.String(30), nullable=False),
        sa.Column('user_id', sa.String(30), sa.ForeignKey('users.id'), nullable=False)
    )


def downgrade():
    op.drop_table('reactions')
