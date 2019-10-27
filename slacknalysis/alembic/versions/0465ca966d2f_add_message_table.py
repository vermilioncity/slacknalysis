"""add message table

Revision ID: 0465ca966d2f
Revises: c856082c1d86
Create Date: 2019-10-27 03:18:31.689172+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0465ca966d2f'
down_revision = 'c856082c1d86'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('ts', sa.Numeric(16, 6), nullable=False, primary_key=True),
        sa.Column('channel_id', sa.String(9), sa.ForeignKey('channels.id')),
        sa.Column('user_id', sa.String(9), sa.ForeignKey('users.id')),
        sa.Column('text', sa.Text(convert_unicode=True), nullable=False),
        sa.Column('reply_count', sa.Integer, nullable=False),
        sa.Column('reply_users_count', sa.Integer, nullable=False),
        sa.Column('thread_ts', sa.Numeric(16, 6))
    )


def downgrade():
    op.drop_table('messages')
