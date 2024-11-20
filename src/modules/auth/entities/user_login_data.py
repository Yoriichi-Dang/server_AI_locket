from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, TIMESTAMP, Text
from sqlalchemy.orm import relationship, sessionmaker
from src.config.database_config import Base
from datetime import datetime


class UsersLoginData(Base):
    __tablename__ = 'users_login_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, onupdate=datetime.utcnow)

    # Relationship
    user_account = relationship("UserAccount", backref="login_data", uselist=False)
