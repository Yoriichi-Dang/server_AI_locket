from sqlalchemy.sql import func
from src.config.database_config import Base
from sqlalchemy import  Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship
from datetime import datetime


class PostCaption(Base):
    __tablename__ = 'post_caption'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    caption = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    # Relationships
    user_posts = relationship("UserPosts", backref="post_caption")
    reactions_list = relationship("PostReactionsList", backref="post_caption")
