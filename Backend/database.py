"""
This file is used to create a database engine and session configuration for the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DATABASE_URL
import psycopg2

# Establish connection using the connection string from config.py
conn = psycopg2.connect(DATABASE_URL)

# Create database engine
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print("Tables created successfully!")