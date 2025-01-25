from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database URL
DATABASE_URL = "sqlite:///./Items.db"

# Create a database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Session configuration
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)