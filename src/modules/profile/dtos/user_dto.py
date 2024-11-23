from pydantic import BaseModel
from typing import Optional
from datetime import date

class UserDto(BaseModel):
    email: str
    phone:str
    username: str
    province: Optional[str] = None  # Optional field with default value `None`
    district: Optional[str] = None  # Optional field with default value `None`
    address: Optional[str] = None  # Optional field with default value `None`
    gender: Optional[str] = None  # Optional field with default value `None`
    day_of_birth: Optional[date] = None  # Optional field with default value `None`
    avatar_url: Optional[str] = None