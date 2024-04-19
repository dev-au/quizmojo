from data.schemas import UserRefreshPhoneModel
from resources.api_response import APIResponse
from resources.authentication import *
from resources.depends import CurrentUser
from urls import user_router


@user_router.patch('/change-phone', response_model=APIResponse.example_model())
async def change_user_phone(user: CurrentUser, user_data: UserRefreshPhoneModel):
    if not verify_password(user_data.password, user.hashed_password):
        raise OldPasswordIncorrectException()
    validate_phone(user_data.new_phone)
    user.phone = user_data.new_phone
    await user.save()
    return APIResponse()
