from src.modules.auth.repository.auth_repository import AuthRepository
from sqlalchemy.orm import Session
from src.modules.auth.dtos.auth_dto import UserRegister,UserLogin
from src.modules.auth.models.user_model import UserModel
from src.utils.auth import verify_password
from src.errors.auth import InvalidPasswordException

class AuthService:
    def __init__(self,db: Session):
        self.auth_repository = AuthRepository(db)
    def register_user(self,user_register:UserRegister):
        user_model=UserModel(
            username=user_register.username,
            phone=user_register.phone,
            email=user_register.email
        )
        id=self.auth_repository.create_account(user_model,user_register.password)
        if id is None:
            return None
        user_model.id=id
        return user_model
    def login_user(self,user_login_dto:UserLogin):
        user_model=UserModel(
            phone=user_login_dto.phone,
        )
        user_login,user= self.auth_repository.get_user_by_phone(user_model.phone)
      
        if not user_login:
            return None
        if verify_password(user_login_dto.password,user_login.password_hash):
            user_model=UserModel(
                id=user.id,
                phone=user_login.phone,
                email=user_login.email,
                username=user.username,
                province=user.province,
                district=user.district,
                address=user.address,
                day_of_birth=user.day_of_birth,
                gender=user.gender,
                avatar_url=user.avatar_url,
            )
            return user_model    
        else:
            raise InvalidPasswordException("Password does not match.")  # Or return a custom message here