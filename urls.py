from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer

user_router = APIRouter(prefix='/user', tags=['User options'])
quiz_router = APIRouter(prefix='/quiz', tags=['Quiz options'])
question_router = APIRouter(prefix='/question', tags=['Question options'])

ROUTERS = (user_router, quiz_router, question_router, )

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login-secret")
