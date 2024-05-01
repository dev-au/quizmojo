from data.exceptions import *
from data.models import Quiz, UserAcceptQuiz, User
from data.schemas import AcceptUserModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from resources.error_docs import error_docs
from urls import quiz_router


@error_docs(QuizNotFoundException, UserNotFoundException)
@quiz_router.post('/accept-user', response_model=APIResponse.example_model())
async def accept_user(user: CurrentUser, user_accept: AcceptUserModel):
    quiz = await Quiz.get_or_none(id=user_accept.quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    accepting_user = await User.get_or_none(username=user_accept.username)
    if not accepting_user:
        raise UserNotFoundException()
    await UserAcceptQuiz.get_or_create(quiz=quiz, user=accepting_user)
    return APIResponse()
