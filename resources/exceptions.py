from fastapi import status, HTTPException

ERRORS: dict = {}


class APIException(HTTPException):

    def __init_subclass__(cls, **kwargs):
        status_code = kwargs.get('status_code')
        cls.status_code = status_code
        ERRORS[cls.__name__] = {'description': cls.__doc__.strip(), 'status_code': status_code}

    def __init__(self):
        super().__init__(self.status_code, {'status_code': self.status_code, 'error': self.__class__.__name__})


class CredentialsException(APIException, status_code=status.HTTP_401_UNAUTHORIZED):
    """
    The user's refresh token has expired or the access token is invalid.
    """


class CaptchaVerifyException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    The provided captcha could not be verified.
    """


class CaptchaExpiredException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    The captcha has expired.
    """


class UserAlreadyExistsException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Attempting to create a user that already exists.
    """


class PasswordConfirmException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    The provided password confirmation does not match the original password.
    """


class PasswordValidationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    The provided password does not meet the required criteria.
    """


class UsernameOrPasswordIncorrectException(APIException, status_code=status.HTTP_401_UNAUTHORIZED):
    """
    The username or password provided during authentication is incorrect.
    """


class OldPasswordIncorrectException(APIException, status_code=status.HTTP_401_UNAUTHORIZED):
    """
    The old password provided for a password update operation is incorrect.
    """
