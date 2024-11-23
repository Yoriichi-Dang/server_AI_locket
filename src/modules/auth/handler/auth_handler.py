from fastapi import APIRouter, Depends, HTTPException,Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from starlette.requests import Request
from src.modules.auth.dtos.auth_dto import UserRegister,UserLogin,Token
from src.config.database_config import connect_db
from src.errors.auth import AccountAlreadyExistsException
from src.utils.auth import verify_token, generate_tokens,get_new_access_token
from datetime import  timedelta
from src.config.auth_config import ConfigAuth
from src.modules.auth.service.auth_service import AuthService
config_auth = ConfigAuth()
router = APIRouter()


@router.post("/register",response_model=Token,tags=['Authenticate'])
async def register(user_register: UserRegister,response: Response, db: Session = Depends(connect_db)):
    try:
        auth_service = AuthService(db)  
        user_model = auth_service.register_user(user_register)
        if user_model is None:
            raise AccountAlreadyExistsException("Account already exists with this email or phone.")
        token=generate_tokens(user_model)
        # Set cookies
        if token is not None:
            response.set_cookie(
                key="access_token",
                value=token.access_token,
                httponly=True,  # Helps mitigate XSS attacks
                max_age=timedelta(minutes=config_auth.access_token_expires).total_seconds(),  # Adjust according to your access token expiration
                path="/"  # Adjust according to your needs
            )
            response.set_cookie(
                key="refresh_token",
                value=token.refresh_token,
                httponly=True,  # Helps mitigate XSS attacks
                max_age=timedelta(days=config_auth.refresh_token_expires).total_seconds(),  # 7 days
                path="/"  # Adjust according to your needs
            )
            return JSONResponse(status_code=201, content=token.dict(),headers=response.headers)
        else:
            return JSONResponse(status_code=400, content={"message":"Token error"})
    
    except AccountAlreadyExistsException:
        raise HTTPException(status_code=400, detail="User with this email or phone already exists")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login",response_model=Token,tags=['Authenticate'])
async def login(user_login:UserLogin,response: Response,db:Session=Depends(connect_db)):
    try:
        auth_service = AuthService(db)
        user_model=auth_service.login_user(user_login)
        token=generate_tokens(user_model)
        # Set cookies
        response.set_cookie(
            key="access_token",
            value=token.access_token,
            httponly=True,  # Helps mitigate XSS attacks
            max_age=timedelta(minutes=config_auth.access_token_expires).total_seconds(),  # Adjust according to your access token expiration
            path="/"  # Adjust according to your needs
        )
        response.set_cookie(
            key="refresh_token",
            value=token.refresh_token,
            httponly=True,  # Helps mitigate XSS attacks
            max_age=timedelta(days=config_auth.refresh_token_expires).total_seconds(),  # 7 days
            path="/"  # Adjust according to your needs
        )
        return JSONResponse(status_code=200, content=token.dict(),headers=response.headers)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post('/refresh_token',tags=['Authenticate'])
async def refresh_token(request:Request):
    try:
        refresh_token=request.cookies.get('refresh_token')
        if not refresh_token:
            raise HTTPException(status_code=400, detail="No refresh token provided")
        if not verify_token(refresh_token):
            raise HTTPException(status_code=400, detail="Invalid refresh token")
        return get_new_access_token(refresh_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))