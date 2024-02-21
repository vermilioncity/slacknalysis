"""add_more_channels

Revision ID: 693d20c5e73d
Revises: 0c9d3fa2c6f7
Create Date: 2020-10-09 20:54:26.887167+00:00

"""
from alembic import op
from sqlalchemy import orm, String, Column, table
from sqlalchemy.sql import insert, delete

# revision identifiers, used by Alembic.
revision = '693d20c5e73d'
down_revision = '0c9d3fa2c6f7'
branch_labels = None
depends_on = None

channels = table('channels',
                 Column('id', String(15), primary_key=True),
                 Column('channel_name', String(30), nullable=False,
                        unique=True))

channel_data = [{'id': 'C018YTEGWQH', 'channel_name': 'humblebrag'},
                {'id': 'C017Y3ZNQ82', 'channel_name': 'what-day-is-it'},
                {'id': 'C01ARL5CWJF', 'channel_name': 'po-west-coast'},
                {'id': 'C016B9TA9FC', 'channel_name': 'po-tography'},
                {'id': 'C015WLP3482', 'channel_name': 'the-expanse'},
                {'id': 'C013TB784PP', 'channel_name': 'po-cartalk'},
                {'id': 'C01271QT3KQ', 'channel_name': 'po-sportstalk'}]

def upgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for channel in channel_data:
        session.execute(insert(channels).values(channel))


def downgrade():
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    for channel in channel_data:
        session.execute(delete(channels).values(channel))
