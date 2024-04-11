import re
from datetime import datetime, timedelta, timezone
from aioredis import Redis
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from data.schemas import *
from data.models import User
from resources.exceptions import *

SECRET_KEY = "1aa7c3c8c5563fb00439b132eb711fe26a36e74b267aa030bbd347fbf2695825"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_captcha(redis: Redis, captcha_key: str, captcha_answer: str):
    real_answer = await redis.get(captcha_key)
    await redis.delete(captcha_key)
    if not real_answer:
        raise CaptchaExpiredException()
    elif int(real_answer) != captcha_answer:
        raise CaptchaVerifyException()


def validate_password(password: str):
    if (len(password) < 8
            or not re.search(r"[a-zA-Z]", password)
            or not re.search(r"\d", password)):
        raise PasswordValidationException()


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def create_user(user_data: SignupModel):
    if user_data.password != user_data.password_confirm:
        raise PasswordConfirmationException()
    if not 5 <= len(user_data.username) <= 16 or not re.match(r'^[a-zA-Z0-9_]+$', user_data.username):
        raise UsernameValidationException()
    validate_password(user_data.password)
    if len(user_data.fullname) > 32:
        raise FullnameValidationException()
    user_exists = await User.exists(username=user_data.username)
    if user_exists:
        raise UserAlreadyExistsException()
    await User.create(
        username=user_data.username,
        fullname=user_data.fullname,
        hashed_password=get_password_hash(user_data.password)
    )


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
