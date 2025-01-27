"""
This file contains the SQLAlchemy models for the database tables. The models are used to create the tables in the database and to define the relationships between them. The models also define the columns and data types for each table.
"""


from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import relationship

Base = declarative_base()
@event.listens_for(Engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    dbapi_connection.execute("PRAGMA foreign_keys=ON")
# Item class (as you already have it)
class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# Conference class
class Conference(Base):
    __tablename__ = "conferences"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    articles = Column(String)  # A simple string that stores a list of articles (or could use a relationship later)

    # Relationship to Articles (one-to-many relationship)
    articles_rel = relationship("Article", back_populates="conference")

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    isbn = Column(String)
    author = Column(String)
    publication_date = Column(String)
    pdf_url = Column(String)
    pdf_texts = Column(String)  # New column to store the content of the PDF texts
    authors = Column(String)
    keywords = Column(String)
    abstract = Column(String)
    location = Column(String)
    start_date = Column(String)
    end_date = Column(String)

    # Foreign Key to link Article to a Conference (allow NULL values)
    conference_id = Column(Integer, ForeignKey('conferences.id', ondelete='SET NULL'), nullable=True)

    # Relationship to Conference (many-to-one relationship)
    conference = relationship("Conference", back_populates="articles_rel")

