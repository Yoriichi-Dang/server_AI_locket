from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from datetime import datetime
from src.config.database_config import Base
from sqlalchemy.orm import relationship

class UsersLoginData(Base):
    __tablename__ = 'users_login_data'
    
    id = Column(Integer, autoincrement=True, primary_key=True)  # Autoincremented primary key
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)
    
    # One-to-one relationship with UserAccount
    user_account = relationship("UserAccount", backref="user_login", uselist=False, cascade="all, delete-orphan")