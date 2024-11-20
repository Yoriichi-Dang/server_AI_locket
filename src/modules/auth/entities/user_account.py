from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship, sessionmaker
from src.config.database_config import Base
from datetime import datetime

class UserAccount(Base):
    __tablename__ = 'users_account'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    avatar_url = Column(String)
    address = Column(String)
    district = Column(String)
    province = Column(String)
    day_of_birth = Column(TIMESTAMP)
    gender = Column(String(6))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    # Relationship
    login_data = relationship("UsersLoginData", backref="user_account", uselist=False)
    posts = relationship("UserPosts", backref="user_account")
    followers = relationship("UsersRelationship", foreign_keys="[UsersRelationship.user_id]", backref="follower", cascade="all, delete-orphan")
    followed = relationship("UsersRelationship", foreign_keys="[UsersRelationship.user_followed_id]", backref="followed", cascade="all, delete-orphan")