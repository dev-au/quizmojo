from typing import Annotated

from fastapi import Request, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from data.exceptions import *
from data.schemas import LoginModel, TokenModel
from resources.api_response import APIResponse
from resources.authentication import authenticate_user, verify_captcha, create_access_token
from resources.error_docs import error_docs
from urls import user_router


@error_docs(UserNotFoundException, CaptchaExpiredException, CaptchaVerifyException)
@user_router.post('/login', response_model=APIResponse.example_model(TokenModel))
async def login_user(request: Request, user_data: LoginModel):
    await verify_captcha(request.app.redis, user_data.captcha_key, user_data.captcha_answer)
    authenticated_user = await authenticate_user(user_data.username, user_data.password)
    if not authenticated_user:
        raise UserNotFoundException()
    access_token = create_access_token(user_data.username)
    return APIResponse(TokenModel(access_token=access_token))


@error_docs(UserNotFoundException, CredentialsException)
@user_router.post('/login-secret')
async def login_user_secret(user_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> TokenModel:
    if not user_data.username.startswith('admin') or not user_data.password == 'admin0890':
        raise CredentialsException()
    authenticated_user = await authenticate_user(user_data.username, user_data.password)
    if not authenticated_user:
        raise UserNotFoundException()
    access_token = create_access_token(user_data.username)
    return TokenModel(access_token=access_token)
