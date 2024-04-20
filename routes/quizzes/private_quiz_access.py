from data.exceptions import *
from data.models import Quiz, UserAcceptQuiz, User
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from urls import quiz_router


@quiz_router.post('/accept-user', response_model=APIResponse.example_model())
async def accept_user(user: CurrentUser, username: str, quiz_id: int):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    accepting_user = await User.get_or_none(username=username)
    if not accepting_user:
        raise UserNotFoundException()
    await UserAcceptQuiz.get_or_create(quiz=quiz, user=accepting_user)
    return APIResponse()
