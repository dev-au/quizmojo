from fastapi import Request

from data.schemas import CaptchaModel
from resources.api_response import *
from resources.captcha_manager import generate_captcha
from urls import user_router


@user_router.get('/generate-captcha', response_model=APIResponse.example_model(CaptchaModel))
async def get_new_captcha(request: Request):
    key, img = await generate_captcha(request.app.redis)
    # answer = str(await request.app.redis.get(key))
    # return APIResponse(CaptchaModel(key=key, img=img), answer=answer)
    return APIResponse(CaptchaModel(key=key, img=img))
