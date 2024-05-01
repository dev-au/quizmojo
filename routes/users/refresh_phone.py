from data.schemas import UserRefreshPhoneModel
from resources.api_response import APIResponse
from resources.authentication import *
from resources.depends import CurrentUser
from resources.error_docs import error_docs
from urls import user_router


@error_docs(OldPasswordIncorrectException, PhoneAlreadyExistsException, PhoneValidationException)
@user_router.patch('/change-phone', response_model=APIResponse.example_model())
async def change_user_phone(user: CurrentUser, user_data: UserRefreshPhoneModel):
    if not verify_password(user_data.password, user.hashed_password):
        raise OldPasswordIncorrectException()
    validate_phone(user_data.new_phone)
    if await User.exists(phone=user_data.new_phone):
        raise PhoneAlreadyExistsException()
    user.phone = user_data.new_phone
    await user.save()
    return APIResponse()
