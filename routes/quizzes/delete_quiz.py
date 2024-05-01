from data.exceptions import *
from data.models import Quiz
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from resources.error_docs import error_docs
from urls import quiz_router


@error_docs(QuizNotFoundException)
@quiz_router.delete('', response_model=APIResponse.example_model())
async def delete_quiz(user: CurrentUser, quiz_id: int):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if quiz:
        await quiz.delete()
        return APIResponse()
    raise QuizNotFoundException()
