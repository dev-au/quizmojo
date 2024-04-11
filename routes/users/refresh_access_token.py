from fastapi import Depends

from data.models import User
from data.schemas import TokenModel
from resources.api_responses import APIResponse
from resources.depends import user_refresh_login
from urls import user_router
from resources.auth import create_access_token


@user_router.get('/refresh', response_model=APIResponse.example_model(TokenModel))
async def refresh_user_access_token(user: User = Depends(user_refresh_login)):
    new_access_token = create_access_token(user.username)
    return APIResponse(TokenModel(access_token=new_access_token))
