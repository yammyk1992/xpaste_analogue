import time

from datetime import datetime, timedelta

from celery import Celery
from sqlalchemy import select, create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Text

celery = Celery('tasks', broker='redis://localhost:6379/0')

engine = create_engine('postgresql+psycopg2://postgres:postgres@localhost:5441/postgres',
                       echo=True,
                       future=True,
                       )
Session = sessionmaker(engine)


@celery.task(name="Delete from db after 24 hours")
def clean_data_after_24_hours():
    with Session() as session:
        query = select(Text).where(Text.death_token == True)
        text_db = session.scalars(query).all()
        while text_db:
            for i in text_db:
                session.delete(i)
            session.commit()
            return "Delete from DB"


@celery.task(name="Delete from db after 3 days")
def clean_data_after_3_days():
    with Session() as session:
        query = select(Text).where(Text.death_token == False)
        text_db = session.scalars(query).all()
        while text_db:
            for i in text_db:
                session.delete(i)
            session.commit()
            return "Delete from DB"
