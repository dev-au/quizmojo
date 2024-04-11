from typing import Union

from pydantic import BaseModel


class UserModel(BaseModel):
    username: str


class SignupModel(UserModel):
    fullname: str
    password: str
    password_confirm: str
    captcha_key: str
    captcha_answer: int


class LoginModel(UserModel):
    password: str
    captcha_key: str
    captcha_answer: int


class TokenModel(BaseModel):
    access_token: str = None
    refresh_token: str = None


class CaptchaData(BaseModel):
    key: str
    img: str


class QuizData(BaseModel):
    id: int
    name: str
