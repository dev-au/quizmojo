from data.schemas import UserRefreshPasswordModel, UserModel
from resources.api_responses import APIResponse
from resources.exceptions import PasswordConfirmException, OldPasswordIncorrectException
from resources.depends import CurrentUser
from resources.auth import authenticate_user, get_password_hash
from urls import user_router


@user_router.post('/refresh-password', response_model=APIResponse.example_model(UserModel))
async def login_user(user: CurrentUser, user_password_data: UserRefreshPasswordModel):
    if user_password_data.new_password != user_password_data.new_password_confirm:
        raise PasswordConfirmException()
    authenticated_user = await authenticate_user(user.username, user_password_data.old_password)
    if not authenticated_user:
        raise OldPasswordIncorrectException()
    user.hashed_password = get_password_hash(user_password_data.new_password)
    await user.save()
    return APIResponse(UserModel(username=user.username, fullname=user.fullname))
