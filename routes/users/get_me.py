from data.schemas import UserModel
from resources.api_responses import APIResponse
from resources.depends import CurrentUser
from urls import user_router


@user_router.get('/getme', response_model=APIResponse.example_model(UserModel))
async def get_user_information(user: CurrentUser):
    return APIResponse(UserModel(username=user.username, fullname=user.fullname))
