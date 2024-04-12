import base64

from captcha.image import ImageCaptcha
import random, uuid
from aioredis import Redis


async def generate_captcha(redis: Redis):
    random_number = str(random.randint(10000, 99999))
    image = ImageCaptcha(height=100)
    captcha_data = image.generate(random_number)
    captcha_bytes = captcha_data.getvalue()
    captcha_base64 = base64.b64encode(captcha_bytes).decode('utf-8')
    captcha_key = str(uuid.uuid4())
    while True:
        if await redis.exists(captcha_key):
            captcha_key = str(uuid.uuid4())
        else:
            break
    await redis.set(captcha_key, random_number, 15 * 60)
    return captcha_key, captcha_base64
