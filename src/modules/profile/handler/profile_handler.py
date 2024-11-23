from fastapi import APIRouter, Depends, HTTPException,Response
from src.modules.profile.dtos.user_dto import UserDto
from starlette.requests import Request
from sqlalchemy.orm import Session
from src.config.database_config import connect_db
from fastapi.responses import JSONResponse
from src.modules.profile.models.user_model import UserModel
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.modules.profile.service.profile_service import ProfileService
from src.utils.auth import hash_password,verify_password
auth_scheme = HTTPBearer()
router = APIRouter()
@router.get('/', response_model=UserDto, tags=['Profile'])
async def get_profile(request: Request, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(connect_db)):
   profile_service=ProfileService(db)
   user_payload = request.state.user
   user_model:UserModel= profile_service.get_user_by_email(user_payload['email'])
   user_dto=UserDto(
      phone=user_model.phone,
      email=user_model.email,
      username=user_model.username,
      province=user_model.province,
      district=user_model.district,
      address=user_model.address,
      day_of_birth=user_model.day_of_birth,
      gender=user_model.gender,
      avatar_url=user_model.avatar_url
   )
   return user_dto
   

@router.put('/', response_model=UserDto, tags=['Profile'])
async def update_profile(request:Request, user_dto:UserDto, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(connect_db)):
   profile_service=ProfileService(db)
   user_payload = request.state.user
   user_model:UserModel= profile_service.get_user_by_email(user_payload['email'])
   user_model.phone=user_dto.phone
   user_model.email=user_dto.email
   user_model.username=user_dto.username
   user_model.province=user_dto.province
   user_model.district=user_dto.district
   user_model.address=user_dto.address
   user_model.day_of_birth=user_dto.day_of_birth
   user_model.gender=user_dto.gender
   user_model.avatar_url=user_dto.avatar_url
   is_success=profile_service.update_user_profile(user_payload['id'],user_model)
   if is_success:
      return JSONResponse(status_code=200,content={"message":"Profile updated successfully"})
   else:
      raise HTTPException(status_code=400, detail="Failed to update profile")
   

@router.put('/update_avatar', tags=['Profile'])
async def update_avatar(request:Request, avatar_url:str, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(connect_db)):
   profile_service=ProfileService(db)
   user_payload = request.state.user
   is_success=profile_service.update_avatar(user_payload['id'],avatar_url)
   if is_success:
      return JSONResponse(status_code=200,content={"message":"Avatar updated successfully"})
   else:
      raise HTTPException(status_code=400, detail="Failed to update avatar")

@router.put('/update_password', tags=['Profile'])
async def update_password(request:Request,old_password:str, new_password:str, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(connect_db)):
   profile_service=ProfileService(db)
   user_payload = request.state.user
   user_model:UserModel= profile_service.get_user_by_email(user_payload['email'])
   if not verify_password(old_password,user_model.password_hash):
      raise HTTPException(status_code=400, detail="Old password is incorrect")
   is_success=profile_service.update_password(user_payload['id'],hash_password(new_password))
   if is_success:
      return JSONResponse(status_code=200,content={"message":"Password updated successfully"})
   else:
      raise HTTPException(status_code=400, detail="Failed to update password")
   
@router.post('/follow', tags=['Profile'])
async def follow_user(request:Request, user_id:str, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(connect_db)):
   profile_service=ProfileService(db)
   user_payload = request.state.user
   if user_payload['id']==user_id:
      raise HTTPException(status_code=400, detail="You can't follow yourself")
   is_success=profile_service.follow_user(user_payload['id'],user_id)
   if is_success:
      return JSONResponse(status_code=200,content={"message":"User followed successfully"})
   else:
      raise HTTPException(status_code=400, detail="Failed to follow user")
   
# @router.post('/unfollow', tags=['Profile'])

@router.get('/friends', tags=['Profile'])
async def get_friends(request:Request, token: HTTPAuthorizationCredentials = Depends(auth_scheme), db: Session = Depends(connect_db)):
   profile_service=ProfileService(db)
   user_payload = request.state.user
   friends=profile_service.get_friends(user_payload['id'])
   return {"friends":friends}