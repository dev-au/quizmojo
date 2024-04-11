from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from data.models import User
from resources.auth import verify_captcha, get_password_hash, validate_password
from urls import user_router
from data.schemas import UserModel, SignupModel
from resources.api_responses import *


@user_router.post('/signup', response_model=APIResponse.example_model(UserModel))
async def signup_user(request: Request, user_data: SignupModel):
    await verify_captcha(request.app.redis, user_data.captcha_key, user_data.captcha_answer)
    if user_data.password != user_data.password_confirm:
        raise PasswordConfirmError()
    if not validate_password(user_data.password):
        raise PasswordValidationError()
    user_exists = await User.exists(username=user_data.username)
    if user_exists:
        raise UserAlreadyExistsError()

    await User.create(
        username=user_data.username,
        fullname=user_data.fullname,
        hashed_password=get_password_hash(user_data.password)
    )

    return APIResponse(UserModel(username=user_data.username), status_code=status.HTTP_201_CREATED)
