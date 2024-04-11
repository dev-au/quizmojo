from typing import Annotated

from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from resources.exceptions import *

from resources.auth import SECRET_KEY, ALGORITHM
from data.models import User
from urls import oauth2_scheme


async def user_refresh_login(refresh_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type: str = payload.get("type")
        if not token_type == 'refresh_token':
            raise CredentialsException()
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
    except JWTError:
        raise CredentialsException()
    user = await User.get_or_none(username=username)
    if user is None:
        raise CredentialsException()
    return user


async def get_current_user(access_token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        token_type: str = payload.get("type")
        if not token_type == 'access_token':
            raise CredentialsException()
        username: str = payload.get("sub")
        if username is None:
            raise CredentialsException()
    except JWTError:
        raise CredentialsException()
    user = await User.get_or_none(username=username)
    if user is None:
        raise CredentialsException()
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
