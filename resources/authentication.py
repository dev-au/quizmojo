from datetime import datetime, timedelta

from jose import jwt

from resources.validators import *
from data.exceptions import *
from data.models import User
from data.schemas import SignupModel
from setup import *


async def create_user(user_data: SignupModel):
    if user_data.password != user_data.password_confirm:
        raise PasswordConfirmationException()
    validate_username(user_data.username)
    validate_password(user_data.password)
    validate_fullname(user_data.fullname)
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
    expire = datetime.now(timezone) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(username: str):
    to_encode = {'sub': username, 'type': 'refresh_token'}
    expire = datetime.now(timezone) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
