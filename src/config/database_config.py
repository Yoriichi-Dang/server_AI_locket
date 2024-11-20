from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.config.server_config import ConfigServer

config = ConfigServer()
engine=create_engine(config.database_url)
SessionLocal=sessionmaker(bind=engine)
Base=declarative_base()

def connect_db():
    return SessionLocal()