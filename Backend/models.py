from sqlalchemy import Column, Integer, String, ForeignKey, TEXT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from pgvector.sqlalchemy import Vector

Base = declarative_base()

# Conference class
class Conference(Base):
    __tablename__ = "conferences"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    articles = Column(ARRAY(String), nullable=True)

    # Relationship to Articles (one-to-many)
    articles_rel = relationship("Article", back_populates="conference", cascade="all, delete-orphan")

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    isbn = Column(String, nullable=True)
    author = Column(String, nullable=True)
    publication_date = Column(String, nullable=True)
    pdf_url = Column(String, nullable=True)
    pdf_texts = Column(TEXT, nullable=True) 
    authors = Column(String, nullable=True)
    keywords = Column(ARRAY(String), nullable=True)
    abstract = Column(String, nullable=True)
    location = Column(String, nullable=True)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    embeddings = Column(Vector(384), nullable=True)  # Use `pgvector` to store embeddings

    # Foreign Key linking to Conference
    conference_id = Column(Integer, ForeignKey('conferences.id', ondelete='SET NULL'), nullable=True)
    
    # Relationship to Conference
    conference = relationship("Conference", back_populates="articles_rel")
