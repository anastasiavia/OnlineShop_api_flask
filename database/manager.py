from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from database.config import *
import mysql.connector


class DBManager:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD
        )
        self.engine = create_engine(
            f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_SCHEMA}"
        )

    def session(self):
        session_factory = sessionmaker(bind=self.engine)
        session = scoped_session(session_factory)
        return session
