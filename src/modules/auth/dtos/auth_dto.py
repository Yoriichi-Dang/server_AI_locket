from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    refresh_token: str
    
class UserLogin(BaseModel):
    phone:str
    password:str

class UserRegister(BaseModel):
    username:str
    phone:str
    email:str
    password:str