# Dette skriptet setter opp SQLite-databasen ved å definere databasebanen, 
# opprette en SQLAlchemy-motor og en session-factory, samt sørge for at alle 
# tabeller definert i models.py blir opprettet.


import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base

# Get absolute path to ensure correct database location
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "database.db")
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"  # Triple slashes are needed for SQLite

# Create database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session factory
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.metadata.create_all(bind=engine)
