import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file (primarily for local development)
load_dotenv()

# 1. Fetch the Database URL from Environment Variables
# Using os.environ.get is safer in production environments like Render
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL")

# 2. Fix for SQLAlchemy compatibility
# Render sometimes provides a URL starting with 'postgres://'
# SQLAlchemy 1.4+ requires 'postgresql://'
if SQLALCHEMY_DATABASE_URL and SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 3. Fallback for Local Development
# If the environment variable is missing, it defaults to your local database
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Shani123@localhost:5432/invoice_db"

# 4. Create the SQLAlchemy engine
# 'pool_pre_ping' helps recover from lost connections (common in cloud environments)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for the models
Base = declarative_base()

# Dependency to get the database session for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()