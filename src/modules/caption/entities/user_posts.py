from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship, sessionmaker
from src.config.database_config import Base
from datetime import datetime

class UserPosts(Base):
    __tablename__ = 'user_posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users_account.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('post_caption.id'), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    # Relationship
    user = relationship("UserAccount", backref="user_posts")
    post_caption = relationship("PostCaption")