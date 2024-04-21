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


class UsernameAlreadyExistsException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Attempting to create a username that already exists.
    """


class PhoneAlreadyExistsException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Attempting to create a phone that already exists.
    """


class UsernameValidationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    User username must be between 5 and 20 characters. And it can only contain alphanumeric characters and underscores.
    """


class FullnameValidationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    User fullname must be 32 characters at most.
    """


class PhoneValidationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    User phone number must be 9 digits.
    """


class PasswordConfirmationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    The provided password confirmation does not match the original password.
    """


class PasswordValidationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    User password must be 8 characters at least. And it must contain numbers and letters.
    """


class OldPasswordIncorrectException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    The old password provided for a password or fullname update operation is incorrect.
    """


class OldAndNewPasswordAreTheSameException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    When a user change own password, the new password is the same as the old one.
    """


class UserNotFoundException(APIException, status_code=status.HTTP_404_NOT_FOUND):
    """
    The user does not exist.
    """


class TooManyRequestsException(APIException, status_code=status.HTTP_429_TOO_MANY_REQUESTS):
    """
    This phone number must be wait 1day.
    """


class QuizNameValidationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Quiz name must be 64 characters at most and 5 characters at least.
    """


class QuizWorkingTimeValidationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Quiz the working time must be 30 seconds at least and 24 hours at most.
    """


class QuizStartingTimeValidationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Quiz the start time must be a time after the current time.
    """


class QuizEndingTimeValidationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Quiz the ending time must be a time after the starting time and also min difference must be at least the
    working time.
    """


class QuizNotFoundException(APIException, status_code=status.HTTP_404_NOT_FOUND):
    """
    Requiring quiz not found.
    """


class QuizExpiredException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Quiz activating time has expired.
    """


class QuizAccessException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    User do not have access for working that quiz.
    """


class QuizAlreadyWorkedException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    User try to work quiz that already worked.
    """


class QuizJoinRequestIsCheckingException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    User already sent join request and quiz creator still not accepted.
    """


class QuizIsNowWorkingException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Quiz has already started working or trying to start quiz from another session or user quit quiz during working.
    """


class QuestionCorrectAnswerValidationException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Question correct answer must be only 1, 2, 3, 4.
    """


class QuestionNotFoundException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Requiring question not found.
    """


class UserNotRegisteredException(APIException, status_code=status.HTTP_400_BAD_REQUEST):
    """
    User not started before sending results.
    """
