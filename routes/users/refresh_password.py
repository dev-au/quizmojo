from fastapi import Request

from data.exceptions import *
from data.schemas import UserRefreshPasswordModel, UserModel
from resources.api_response import APIResponse
from resources.authentication import authenticate_user, get_password_hash, verify_captcha, validate_password
from resources.depends import CurrentUser
from urls import user_router


@user_router.patch('/change-password', response_model=APIResponse.example_model(UserModel))
async def refresh_user_password(request: Request, user: CurrentUser, user_password_data: UserRefreshPasswordModel):
    await verify_captcha(request.app.redis, user_password_data.captcha_key, user_password_data.captcha_answer)
    if user_password_data.new_password != user_password_data.new_password_confirm:
        raise PasswordConfirmationException()
    if not validate_password(user_password_data.new_password):
        raise PasswordValidationException()
    authenticated_user = await authenticate_user(user.username, user_password_data.old_password)
    if not authenticated_user:
        raise OldPasswordIncorrectException()
    elif user_password_data.old_password == user_password_data.new_password:
        raise OldAndNewPasswordAreTheSameException()
    user.hashed_password = get_password_hash(user_password_data.new_password)
    await user.save()
    return APIResponse(UserModel(username=user.username, fullname=user.fullname))
