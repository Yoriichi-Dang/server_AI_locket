from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from src.config.database_config import Base
from datetime import datetime

class UserAccount(Base):
    __tablename__ = 'users_account'
    
    id = Column(Integer, ForeignKey('users_login_data.id'), primary_key=True)
    username = Column(String)
    avatar_url = Column(String)
    address = Column(String)
    district = Column(String)
    province = Column(String)
    day_of_birth = Column(TIMESTAMP)
    gender = Column(String(6))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)
