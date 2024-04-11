from fastapi import Request
from data.models import User
from resources.auth import verify_captcha, get_password_hash, validate_password
from data.schemas import UserModel, SignupModel
from resources.exceptions import *
from resources.api_responses import APIResponse
from urls import user_router


@user_router.post('/signup', response_model=APIResponse.example_model(UserModel))
async def signup_user(request: Request, user_data: SignupModel):
    await verify_captcha(request.app.redis, user_data.captcha_key, user_data.captcha_answer)
    if user_data.password != user_data.password_confirm:
        raise PasswordConfirmException()
    if not validate_password(user_data.password):
        raise PasswordValidationException()
    user_exists = await User.exists(username=user_data.username)
    if user_exists:
        raise UserAlreadyExistsException()

    await User.create(
        username=user_data.username,
        fullname=user_data.fullname,
        hashed_password=get_password_hash(user_data.password)
    )

    return APIResponse(UserModel(username=user_data.username, fullname=user_data.fullname),
                       status_code=status.HTTP_201_CREATED)
