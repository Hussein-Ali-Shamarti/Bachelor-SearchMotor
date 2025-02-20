"""
This file is used to create a database engine and session configuration for the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)  # Ensure stable connection

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to initialize database (only run manually, not on every import)
def init_db():
    Base.metadata.create_all(engine)
    print("✅ Tables created successfully!")

print("✅ Database engine connected!")
