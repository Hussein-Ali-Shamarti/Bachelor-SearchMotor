from sqlalchemy import Column, Integer, String, ForeignKey, TEXT, BLOB, JSON, event
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import Engine

Base = declarative_base()

@event.listens_for(Engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    dbapi_connection.execute("PRAGMA foreign_keys=ON")

# Conference class
class Conference(Base):
    __tablename__ = "conferences"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    articles = Column(JSON, nullable=True)  # Changed from ARRAY to JSON

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
    pdf_texts = Column(BLOB, nullable=True) 
    keywords = Column(JSON, nullable=True)  # Changed from ARRAY to JSON
    abstract = Column(String, nullable=True)
    location = Column(String, nullable=True)
    start_date = Column(String, nullable=True)
    end_date = Column(String, nullable=True)
    embeddings = Column(BLOB, nullable=True)  # Adjust as needed

    # Foreign Key linking to Conference
    conference_id = Column(Integer, ForeignKey('conferences.id', ondelete='SET NULL'), nullable=True)
    
    # Relationship to Conference
    conference = relationship("Conference", back_populates="articles_rel")
