import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_url():
    base_url = 'postgresql+psycopg2://{username}:{password}@{service}:{port}/{name}'
    db_url = base_url.format(username=os.getenv('DB_USER'),
                             password=os.getenv('DB_PW'),
                             service=os.getenv('DB_SERVICE'),
                             port=os.getenv('DB_PORT'),
                             name=os.getenv('DB_NAME'))
    return db_url


db_url = get_db_url()
engine = create_engine(db_url)

Base = declarative_base()
Base.metadata.bind = engine

Session = sessionmaker(bind=engine)
session = Session()

