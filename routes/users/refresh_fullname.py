from data.schemas import UserRefreshFullnameModel, UserModel
from resources.api_response import APIResponse
from resources.authentication import *
from resources.depends import CurrentUser
from urls import user_router


@user_router.patch('/change-fullname', response_model=APIResponse.example_model(UserModel))
async def change_user_fullname(user: CurrentUser, user_data: UserRefreshFullnameModel):
    if not verify_password(user_data.password, user.hashed_password):
        raise OldPasswordIncorrectException()
    validate_fullname(user_data.new_fullname)
    user.fullname = user_data.new_fullname
    await user.save()
    return APIResponse(UserModel(username=user.username, fullname=user.fullname))
