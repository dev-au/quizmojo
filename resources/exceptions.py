from fastapi import status, HTTPException

ERRORS: dict = {}


class APIException(HTTPException):
    status_code: int

    def __init_subclass__(cls):
        variables = cls.__dict__
        cls.status_code = variables.get('status_code')
        ERRORS[cls.__name__] = {'description': cls.__doc__.strip(), 'status_code': cls.status_code}

    def __init__(self):
        super().__init__(self.status_code, {'status_code': self.status_code, 'error': self.__class__.__name__})


class CredentialsException(APIException):
    """
    The user's refresh token has expired or the access token is invalid.
    """
    status_code = status.HTTP_401_UNAUTHORIZED


class CaptchaVerifyException(APIException):
    """
    The provided captcha could not be verified.
    """
    status_code = status.HTTP_400_BAD_REQUEST


class CaptchaExpiredException(APIException):
    """
    The captcha has expired.
    """
    status_code = status.HTTP_400_BAD_REQUEST


class UserAlreadyExistsException(APIException):
    """
    Attempting to create a user that already exists.
    """
    status_code = status.HTTP_400_BAD_REQUEST


class PasswordConfirmException(APIException):
    """
    The provided password confirmation does not match the original password.
    """
    status_code = status.HTTP_400_BAD_REQUEST


class PasswordValidationException(APIException):
    """
    The provided password does not meet the required criteria.
    """
    status_code = status.HTTP_400_BAD_REQUEST


class UsernameOrPasswordIncorrectException(APIException):
    """
    The username or password provided during authentication is incorrect.
    """
    status_code = status.HTTP_401_UNAUTHORIZED


class OldPasswordIncorrectException(APIException):
    """
    The old password provided for a password update operation is incorrect.
    """
    status_code = status.HTTP_401_UNAUTHORIZED
