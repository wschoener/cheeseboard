import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "bad_url")

engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def init_db():
    """Create all tables from models. Call once on first run."""
    from models import run, fit_data, runner  # noqa: F401

    Base.metadata.create_all(engine)
    print("Database initialized.")

def wipe_db():
    """Drop all tables. Use with caution!""" 
    Base.metadata.drop_all(engine, checkfirst=True)
    print("Database wiped.")
