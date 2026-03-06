from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


# Database connection URL
DATABASE_URL = os.getenv("DATABASE_URL")


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)


# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for models
Base = declarative_base()


# Dependency for getting DB session
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()