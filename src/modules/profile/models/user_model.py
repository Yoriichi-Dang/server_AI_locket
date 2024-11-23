from pydantic import BaseModel
from typing import Optional
from datetime import date
from dataclasses import dataclass

@dataclass
class UserModel:
    id: int=0
    phone: str=""
    email: str = ""
    username: str = ""
    province: str = ""
    district: str = ""
    address: str = ""
    day_of_birth: Optional[date] = None
    gender: str = ""
    avatar_url: str = ""
    password_hash: str = ""