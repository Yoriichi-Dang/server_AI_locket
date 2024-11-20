from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship, sessionmaker
from src.config.database_config import Base
from datetime import datetime

class UsersRelationship(Base):
    __tablename__ = 'users_relationship'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users_account.id'), nullable=False)
    user_followed_id = Column(Integer, ForeignKey('users_account.id'), nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    # Relationships to UserAccount (followers and followed users)
    user = relationship("UserAccount", foreign_keys=[user_id], backref="followers")
    followed_user = relationship("UserAccount", foreign_keys=[user_followed_id], backref="followed_by")