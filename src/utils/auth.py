# src/auth.py
import jwt
import bcrypt
from datetime import datetime, timedelta
from typing import Optional
from src.config.auth_config import ConfigAuth
from src.modules.auth.dtos.auth_dto import Token
from src.modules.auth.models.user_model import UserModel

config_auth = ConfigAuth()
def get_new_access_token(refresh_token: str) -> Token:
    payload = decode_access_token(refresh_token)
    if not payload:
        return None
    user = UserModel(id=payload["id"],email=payload["email"])
    token = create_token(data={"id": user.id, "email": user.email})
    return Token(access_token=token, refresh_token=refresh_token)

def verify_token(token: str) -> bool:
    try:
        payload = jwt.decode(token, config_auth.secret_key, algorithms=[config_auth.algorithm])
        if datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
            return False
        # Kiểm tra các trường khác nếu cần
        if "email" not in payload:
            return False
        return True
    except jwt.ExpiredSignatureError:
        return False
    except jwt.PyJWTError:
        return False


def generate_tokens(user_model: UserModel) -> Token:
    access_token = create_token(data={"id": user_model.id, "email": user_model.email})
    refresh_token = create_token(data={"id": user_model.id,"email": user_model.email}, expires_delta=timedelta(days=7))
    return Token(access_token=access_token, refresh_token=refresh_token)

def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=config_auth.access_token_expires)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config_auth.secret_key, algorithm=config_auth.algorithm)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, config_auth.secret_key, algorithms=[config_auth.algorithm])
        return payload
    except jwt.PyJWTError:
        return None
    
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))