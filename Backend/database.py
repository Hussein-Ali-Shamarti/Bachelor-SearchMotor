"""
This file is used to create a database engine and session configuration for the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# NEON PostgreSQL database URL
DATABASE_URL = "INSERT NEON DATABASE URL HERE"

# Create database engine
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(engine)

print("Tables created successfully!")