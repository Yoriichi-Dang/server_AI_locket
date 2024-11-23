from sqlalchemy.orm import Session
from src.modules.auth.entities.user_account import UserAccount
from src.modules.auth.entities.user_login_data import UsersLoginData
from src.modules.profile.models.user_model import UserModel
from sqlalchemy.exc import SQLAlchemyError
from src.errors.auth import *
from src.modules.profile.entities.users_relationship import UsersRelationship

class ProfileRepository:
    def __init__(self,db:Session) -> None:
        self.db=db
    def get_user_by_email(self,email:str):
        try:
        # Join UsersLoginData and UserAccount based on their common id
            user_with_login = self.db.query(UsersLoginData, UserAccount).\
                join(UserAccount, UsersLoginData.id == UserAccount.id).\
                filter(UsersLoginData.email == email).\
                first()
            if user_with_login:
                user_login, user = user_with_login
                user_model:UserModel=UserModel(
                    id=user_login.id,
                    phone=user_login.phone,
                    email=user_login.email,
                    username=user.username,
                    province=user.province,
                    district=user.district,
                    address=user.address,
                    day_of_birth=user.day_of_birth,
                    gender=user.gender,
                    avatar_url=user.avatar_url,
                    password_hash=user_login.password_hash
                )
                return user_model
            else:
                # Handle the case when no user is found
                raise AccountNotFoundException("User not found with this phone number.")
    
        except AccountNotFoundException as e:
            raise e
        except SQLAlchemyError as e:
            raise e
        finally:
            self.db.close()
    def update_user_profile(self, id: str, user_model: UserModel):
        try:
            # Update UserAccount fields if the new value exists, else keep the old value
            rows_updated = self.db.query(UserAccount).\
                filter(UserAccount.id == id).\
                update({
                    UserAccount.username: user_model.username or UserAccount.username,
                    UserAccount.province: user_model.province or UserAccount.province,
                    UserAccount.district: user_model.district or UserAccount.district,
                    UserAccount.address: user_model.address or UserAccount.address,
                    UserAccount.day_of_birth: user_model.day_of_birth or UserAccount.day_of_birth,
                    UserAccount.gender: user_model.gender or UserAccount.gender,
                }, synchronize_session=False)

            # Commit the update
            self.db.commit()

            # Check if any rows were updated
            if rows_updated == 0:
                raise AccountNotFoundException("User not found with this email.")

            # Update UsersLoginData fields if necessary
            rows_updated_login = self.db.query(UsersLoginData).\
                filter(UsersLoginData.id == id).\
                update({
                    UsersLoginData.phone: user_model.phone or UsersLoginData.phone,
                    UsersLoginData.email: user_model.email or UsersLoginData.email
                }, synchronize_session=False)

            # Commit the update
            self.db.commit()

            if rows_updated_login == 0:
                raise AccountNotFoundException("User login data not found.")
            
            return True  # Return success status

        except AccountNotFoundException as e:
            raise e
        except SQLAlchemyError as e:
            # Handle database error, rollback transaction if something goes wrong
            self.db.rollback()
            raise e
        finally:
            self.db.close()
    def update_avatar(self, id: str, avatar_url: str):
        try:
            # Update UserAccount avatar_url field
            rows_updated = self.db.query(UserAccount).\
                filter(UserAccount.id == id).\
                update({
                    UserAccount.avatar_url: avatar_url
                }, synchronize_session=False)

            # Commit the update
            self.db.commit()

            # Check if any rows were updated
            if rows_updated == 0:
                raise AccountNotFoundException("User not found with this email.")

            return True  # Return success status

        except AccountNotFoundException as e:
            raise e
        except SQLAlchemyError as e:
            # Handle database error, rollback transaction if something goes wrong
            self.db.rollback()
            raise e
        finally:
            self.db.close()
    def update_password(self,id:str,new_password:str):
        try:
            # Update UsersLoginData password_hash field
            rows_updated = self.db.query(UsersLoginData).\
                filter(UsersLoginData.id == id).\
                update({
                    UsersLoginData.password_hash: new_password
                }, synchronize_session=False)

            # Commit the update
            self.db.commit()

            # Check if any rows were updated
            if rows_updated == 0:
                raise AccountNotFoundException("User login data not found.")

            return True  # Return success status

        except AccountNotFoundException as e:
            raise e
        except SQLAlchemyError as e:
            # Handle database error, rollback transaction if something goes wrong
            self.db.rollback()
            raise e
        finally:
            self.db.close()

    def follow_user(self, user_id: str, user_followed_id: str):
        try:
            relationship = UsersRelationship(
                user_id=user_id,
                user_followed_id=user_followed_id
            )
            self.db.add(relationship)
            self.db.commit()
            return True  # Return success status
        except SQLAlchemyError as e:
            # Handle database error, rollback transaction if something goes wrong
            self.db.rollback()
            return False 
        finally:
            self.db.close()
    def get_list_friends(self, user_id: str):
        try:
            # Query to find users who follow the given user and are followed back by the user
            friends = self.db.query(UserAccount).\
                join(UsersRelationship, UsersRelationship.user_followed_id == UserAccount.id).\
                filter(UsersRelationship.user_id == user_id).\
                filter(UsersRelationship.user_followed_id == user_id).\
                all()

            # Get the list of users the current user follows
            followed_users = self.db.query(UserAccount).\
                join(UsersRelationship, UsersRelationship.user_id == UserAccount.id).\
                filter(UsersRelationship.user_followed_id == user_id).\
                all()

            # Combine both lists of friends (followers and followed users)
            mutual_friends = []

            for user in followed_users:
                # Check if this followed user is also following back
                mutual_friend = self.db.query(UsersRelationship).\
                    filter(UsersRelationship.user_id == user.id).\
                    filter(UsersRelationship.user_followed_id == user_id).\
                    first()

                if mutual_friend:
                    mutual_friends.append(user)

            return mutual_friends

        except SQLAlchemyError as e:
            # Handle database error
            raise e