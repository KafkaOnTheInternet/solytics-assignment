from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Local params
load_dotenv()

# Get Postgres running
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(os.environ.get('DB_URL')))
Base = declarative_base()

# Pass around to manipulate db
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()