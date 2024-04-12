import re
from aioredis import Redis
from passlib.context import CryptContext
from data.exceptions import *

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def verify_captcha(redis: Redis, captcha_key: str, captcha_answer: int):
    real_answer = await redis.get(captcha_key)
    await redis.delete(captcha_key)
    if not real_answer:
        raise CaptchaExpiredException()
    elif int(real_answer) != captcha_answer:
        raise CaptchaVerifyException()


def validate_password(password: str):
    if (len(password) < 8
            or not re.search(r"[a-zA-Z]", password)
            or not re.search(r"\d", password)):
        raise PasswordValidationException()


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def validate_username(username: str):
    if not 5 <= len(username) <= 16 or not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise UsernameValidationException()


def validate_fullname(fullname: str):
    if len(fullname) > 32:
        raise FullnameValidationException()
