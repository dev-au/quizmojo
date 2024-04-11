import json

from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class APIResponse(JSONResponse):

    def __init__(self, model: BaseModel = None, detail: str = 'success', status_code: int = 200, **kwargs):
        json_data = {}
        if model:
            json_data.update(model)
        if kwargs:
            json_data.update(kwargs)
        response_content = {'status_code': status_code, 'detail': detail, 'data': json_data}
        super().__init__(status_code=status_code, content=response_content)

    @staticmethod
    def example_model(model: BaseModel):
        class ResponseModel(BaseModel):
            status_code: int
            detail: str
            data: model

        return ResponseModel


class APIException(HTTPException):
    status_code: int
    detail: str

    def __init_subclass__(cls):
        variables = cls.__dict__
        cls.status_code = variables.get('status_code')
        cls.detail = variables.get('detail')

    def __init__(self):
        super().__init__(self.status_code, self.detail)


class CredentialsError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'invalid_credentials'


class CaptchaVerifyError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'captcha_verify_error'


class CaptchaExpiredError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'captcha_expired_error'


class UserAlreadyExistsError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'user_already_exists_error'


class PasswordConfirmError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'password_confirm_error'


class PasswordValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'password_validation_error'
