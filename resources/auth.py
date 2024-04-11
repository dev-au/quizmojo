import re
from datetime import datetime, timedelta, timezone
from aioredis import Redis
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from data.schemas import *
from data.models import User
from resources.api_responses import *

SECRET_KEY = "1aa7c3c8c5563fb00439b132eb711fe26a36e74b267aa030bbd347fbf2695825"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_captcha(redis: Redis, captcha_key: str, captcha_answer: str):
    real_answer = await redis.get(captcha_key)
    await redis.delete(captcha_key)
    if not real_answer:
        raise CaptchaExpiredError()
    elif int(real_answer) != captcha_answer:
        raise CaptchaVerifyError()


def validate_password(password: str):
    return False if len(password) < 8 or not re.search(r"[a-zA-Z]", password) or not re.search(r"\d",
                                                                                               password) else True


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str):
    user = await User.get_or_none(username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str):
    to_encode = {'sub': username, 'type': 'access_token'}
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(username: str):
    to_encode = {'sub': username, 'type': 'refresh_token'}
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


