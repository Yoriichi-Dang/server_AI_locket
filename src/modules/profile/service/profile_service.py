from sqlalchemy.orm import Session
from src.modules.profile.models.user_model import UserModel
from src.modules.profile.repository.profile_repository import ProfileRepository
class ProfileService:
    def __init__(self,db:Session) -> None:
        self.profile_repository=ProfileRepository(db)
    def get_user_by_email(self,email:str)->UserModel:
        try:
            user_model=self.profile_repository.get_user_by_email(email)
            return user_model
        except Exception as e:
            raise e
    def update_user_profile(self,id:str,user_model:UserModel)->bool:
        try:
            is_success=self.profile_repository.update_user_profile(id,user_model)
            return is_success
        except Exception as e:
            raise e
    def update_avatar(self,id:str,avatar_url:str)->bool:
        try:
            is_success=self.profile_repository.update_avatar(id,avatar_url)
            return is_success
        except Exception as e:
            raise e
    def update_password(self,id:str,password:str)->bool:
        try:
            is_success=self.profile_repository.update_password(id,password)
            return is_success
        except Exception as e:
            raise e
    def follow_user(self,id:str,follow_id:str)->bool:
        try:
            is_success=self.profile_repository.follow_user(id,follow_id)
            return is_success
        except Exception as e:
            raise e
    def get_friends(self,id:str)->list:
        try:
            friends=self.profile_repository.get_list_friends(id)
            return friends
        except Exception as e:
            raise e