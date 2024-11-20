from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship, sessionmaker
from src.config.database_config import Base
from datetime import datetime

class PostReactionsList(Base):
    __tablename__ = 'post_reactions_list'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    post_caption_id = Column(Integer, ForeignKey('post_caption.id'), nullable=False)
    post_reaction_id = Column(Integer, ForeignKey('post_reaction.id'), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    # Relationships to PostCaption and PostReaction
    post_caption = relationship("PostCaption", backref="reactions_list")
    post_reaction = relationship("PostReaction", backref="reactions_list")
