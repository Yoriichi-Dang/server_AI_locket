from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv()

class ConfigAuth(BaseSettings):
    secret_key:str=os.getenv('SECRET_KEY')
    algorithm:str=os.getenv('ALGORITHM')
    access_token_expires:int=os.getenv('ACCESS_TOKEN_EXPIRE')
    refresh_token_expires:int=os.getenv('REFRESH_TOKEN_EXPIRE')