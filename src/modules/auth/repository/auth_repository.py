
from src.modules.auth.entities.user_login_data import UsersLoginData
from src.modules.auth.entities.user_account import UserAccount
from src.modules.auth.models.user_model import UserModel
from src.errors.auth import *
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from src.utils.auth import hash_password
class AuthRepository:
    def __init__(self,db:Session):
        self.db = db
    def create_account(self, user_model: UserModel, password: str):
        try:
            # Check if the user already exists based on phone or email
            existing_user = self.db.query(UsersLoginData).filter(
                (UsersLoginData.phone == user_model.phone) | (UsersLoginData.email == user_model.email)
            ).first()

            if existing_user:
                raise AccountAlreadyExistsException("Account already exists with this email or phone.")
            
            # Hash the password before saving
            password_hash = hash_password(password)
            
            # Create a new UsersLoginData instance
            user_login = UsersLoginData(
                phone=user_model.phone,
                email=user_model.email,
                password_hash=password_hash,
            )
            self.db.add(user_login)
            self.db.commit()  # Commit here to generate the user_login.id
            self.db.refresh(user_login)

            # Create the associated UserAccount instance, using the same id from UsersLoginData
            user_account = UserAccount(
                id=user_login.id,  # Use the same id from UsersLoginData
                username=user_model.username,
            )
            
            # Link the user_login to the user_account via relationship
            user_account.user_login = user_login  # This sets the relationship
            self.db.add(user_account)
            self.db.commit()  # Commit the UserAccount with the linked id
            self.db.refresh(user_account)
            
            return user_account.id
        except AccountAlreadyExistsException as e:
            raise e  # Raise specific exception for existing account
        except SQLAlchemyError as e:
            self.db.rollback()  # Rollback in case of any error
            print(e)
            raise e
        finally:
            self.db.close()  # Ensure the session is closed
    
    def get_user_by_phone(self, phone: str):
        try:
        # Join UsersLoginData and UserAccount based on their common id
            user_with_login = self.db.query(UsersLoginData, UserAccount).\
                join(UserAccount, UsersLoginData.id == UserAccount.id).\
                filter(UsersLoginData.phone == phone).\
                first()
            if user_with_login:
                user_login, user = user_with_login
                return user_login, user
            else:
                # Handle the case when no user is found
                raise AccountNotFoundException("User not found with this phone number.")
    
        except AccountNotFoundException as e:
            raise e
        except SQLAlchemyError as e:
            raise e
        finally:
            self.db.close()
   
    
   
