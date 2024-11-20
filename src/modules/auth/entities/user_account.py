from sqlalchemy import Column, Integer, String, TIMESTAMP,ForeignKey
from datetime import datetime
from src.config.database_config import Base
from sqlalchemy.orm import relationship

class UserAccount(Base):
    __tablename__ = 'users_account'
    
    id = Column(Integer, ForeignKey('users_login_data.id'), primary_key=True)  # UserAccount.id is a ForeignKey that refers to UsersLoginData.id
    username = Column(String)
    avatar_url = Column(String)
    address = Column(String)
    district = Column(String)
    province = Column(String)
    day_of_birth = Column(TIMESTAMP)
    gender = Column(String(6))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    # # One-to-many relationship: One user can have multiple posts
    # posts = relationship("UserPosts", backref="user_account", cascade="all, delete-orphan")
    
    # # One-to-many relationship for followers and followed users
    # followers = relationship("UsersRelationship", foreign_keys="[UsersRelationship.user_id]", backref="follower", cascade="all, delete-orphan")
    # followed = relationship("UsersRelationship", foreign_keys="[UsersRelationship.user_followed_id]", backref="followed", cascade="all, delete-orphan")