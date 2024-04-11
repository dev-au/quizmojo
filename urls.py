from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

user_router = APIRouter(prefix='/user', tags=['User options'])
captcha_router = APIRouter(prefix='/captcha', tags=['Captcha options'])

ROUTERS = (user_router, captcha_router, )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")
