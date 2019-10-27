from sqlalchemy import Column, Integer, String, Numeric, Text, ForeignKey

from slack_scraper.db import Base
from slack_scraper.utils import convert_timestamp_to_est


class User(Base):
    __tablename__ = 'users'
    id = Column(String(9), primary_key=True)
    name = Column(String(30), nullable=False)

    def __repr__(self):
        return "<User(id='%s', name='%s')>" % (self.id, self.name)


class Channel(Base):
    __tablename__ = 'channels'
    id = Column(String(9), primary_key=True)
    name = Column(String(30), nullable=False)

    def __repr__(self):
        return "<Channel(id='%s', name='%s')>" % (self.id, self.name)


class Message(Base):
    __tablename__ = 'messages'
    channel_id = Column(String(9), ForeignKey('channels.id'))
    ts = Column(Numeric(16, 6), primary_key=True)
    user_id = Column(String(9), ForeignKey('users.id'))
    text = Column(Text(), nullable=False)
    thread_ts = Column(Numeric(16, 6))
    reply_count = Column(Integer, nullable=False)
    reply_users_count = Column(Integer, nullable=False)

    def __repr__(self):
        return "<Message(id='%s', text='%s', ts='%s')>" % (self.id, self.text, convert_timestamp_to_est(self.ts))


class Reaction(Base):
    __tablename__ = 'reactions'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    message_ts = Column(Integer, ForeignKey('messages.ts'), nullable=False)
    name = Column(String(50), nullable=False)
    user_id = Column(String(30), ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return "<Reaction(name='%s', user_id='%s')>" % (self.name, self.user_id)


class Giphy(Base):
    __tablename__ = 'giphys'
    id = Column(Integer, primary_key=True)
    message_ts = Column(Numeric(16, 6), ForeignKey('messages.ts'), nullable=False)
    title = Column(String(50), nullable=False)
    image_url = Column(String(200), nullable=False)

    def __repr__(self):
        return "<Giphy(title='%s', image_url='%s')>" % (self.title, self.image_url)
