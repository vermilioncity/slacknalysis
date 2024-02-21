"""add channel tables

Revision ID: c856082c1d86
Revises: af83a7904c99
Create Date: 2019-10-27 03:17:28.290862+00:00

"""
from alembic import op
import sqlalchemy as sa

import json
import os

# revision identifiers, used by Alembic.
revision = 'c856082c1d86'
down_revision = 'af83a7904c99'
branch_labels = None
depends_on = None


def _get_channel_json_path(file):
    parent_dir, _ = os.path.split(file)
    json_path = os.path.join(parent_dir, 'channels', 'channels.json')

    return json_path


def upgrade():
    table = op.create_table('channels',
                            sa.Column('id', sa.String(15), primary_key=True),
                            sa.Column('channel_name', sa.String(30), nullable=False, unique=True))

    json_path = _get_channel_json_path(__file__)
    with open(json_path) as f:
        channels = json.load(f)
        op.bulk_insert(table, channels)


def downgrade():
    op.drop_table('channels')
