from aioredis import Redis
from fastapi import Request

from resources.captcha_manager import generate_captcha
from data.schemas import CaptchaData
from urls import captcha_router
from resources.api_responses import *


@captcha_router.get('/generate', response_model=APIResponse.example_model(CaptchaData))
async def get_new_captcha(request: Request):
    key, img = await generate_captcha(request.app.redis)
    return APIResponse(CaptchaData(key=key, img=img))
