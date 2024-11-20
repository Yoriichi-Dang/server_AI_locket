from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship, sessionmaker
from src.config.database_config import Base
from datetime import datetime
class PostReaction(Base):
    __tablename__ = 'post_reaction'
    id = Column(Integer, primary_key=True, autoincrement=True)
    comment = Column(String)
    icon = Column(String)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    # Relationship
    reactions_list = relationship("PostReactionsList", backref="reaction", cascade="all, delete-orphan")
