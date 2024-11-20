from sqlalchemy.sql import func
from src.config.database_config import Base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

class PostCaption(Base):
    __tablename__ = 'post_caption'
    id = Column(Integer, primary_key=True, autoincrement=True)
    caption = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    # Relationship
    reactions = relationship("PostReactionsList", backref="post_caption", cascade="all, delete-orphan")

