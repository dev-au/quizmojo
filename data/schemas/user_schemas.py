from pydantic import BaseModel


class UserModel(BaseModel):
    username: str
    phone: int
    fullname: str


class SignupModel(BaseModel):
    username: str
    phone: int
    fullname: str
    password: str
    captcha_key: str
    captcha_answer: int


class LoginModel(BaseModel):
    username: str
    password: str
    captcha_key: str
    captcha_answer: int


class UserRefreshPasswordModel(BaseModel):
    old_password: str
    new_password: str
    captcha_key: str
    captcha_answer: int


class UserRefreshFullnameModel(BaseModel):
    new_fullname: str
    password: str


class UserRefreshPhoneModel(BaseModel):
    new_phone: int
    password: str


class TokenModel(BaseModel):
    access_token: str = None
    token_type: str = 'Bearer'


class CaptchaModel(BaseModel):
    key: str
    img: str


class AcceptUserModel(BaseModel):
    username: str
    quiz_id: int
