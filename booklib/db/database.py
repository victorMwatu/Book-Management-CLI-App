from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from booklib.db.models import Base

DATABASE_URL = "sqlite:///booklib.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)