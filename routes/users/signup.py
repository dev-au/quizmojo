from fastapi import Request

from data.exceptions import *
from data.schemas import SignupModel, TokenModel
from resources.api_response import APIResponse
from resources.authentication import create_user, verify_captcha, create_access_token
from resources.error_docs import error_docs
from urls import user_router


@error_docs(PhoneAlreadyExistsException, UsernameAlreadyExistsException, CaptchaVerifyException,
            CaptchaExpiredException, PhoneValidationException, FullnameValidationException, UsernameValidationException,
            PasswordValidationException)
@user_router.post('/signup', response_model=APIResponse.example_model(TokenModel))
async def signup_user(request: Request, user_data: SignupModel):
    await verify_captcha(request.app.redis, user_data.captcha_key, user_data.captcha_answer)
    await create_user(user_data)
    access_token = create_access_token(user_data.username)
    return APIResponse(TokenModel(access_token=access_token))
