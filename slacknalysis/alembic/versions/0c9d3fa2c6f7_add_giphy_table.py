"""add giphy table

Revision ID: 0c9d3fa2c6f7
Revises: e40505630c39
Create Date: 2019-10-27 06:28:16.361509+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c9d3fa2c6f7'
down_revision = 'e40505630c39'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'giphys',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('message_ts', sa.Numeric(16, 6), sa.ForeignKey('messages.ts'), nullable=False),
        sa.Column('title', sa.String(30), nullable=False),
        sa.Column('image_url', sa.String(200), nullable=False)
    )


def downgrade():
    op.drop_table('giphys')
