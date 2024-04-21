from fastapi import Request

from data.exceptions import UserNotFoundException
from data.schemas import LoginModel, TokenModel
from resources.api_response import APIResponse
from resources.authentication import authenticate_user, verify_captcha, create_access_token, create_refresh_token
from urls import user_router


@user_router.post('/login', response_model=APIResponse.example_model(TokenModel))
async def login_user(request: Request, user_data: LoginModel):
    await verify_captcha(request.app.redis, user_data.captcha_key, user_data.captcha_answer)
    authenticated_user = await authenticate_user(user_data.username, user_data.password)
    if not authenticated_user:
        raise UserNotFoundException()
    access_token = create_access_token(user_data.username)
    refresh_token = create_refresh_token(user_data.username)
    return APIResponse(TokenModel(access_token=access_token, refresh_token=refresh_token))



