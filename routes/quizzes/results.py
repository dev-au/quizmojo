from data.exceptions import *
from data.models import Quiz, ResultQuiz
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from urls import quiz_router


@quiz_router.get('/results', response_model=APIResponse.example_model())
async def result_quizzes(user: CurrentUser, quiz_id: int, page: int):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    await ResultQuiz.finish_latecomers(quiz_id)
    results = await ResultQuiz.filter(quiz=quiz, corrects__ne=-1)
    offset = (page - 1) * 10
    if quiz.is_forever:
        results = sorted(results, key=lambda x: (-x.corrects, x.ended_time - x.started_time))
    else:
        results = sorted(results, key=lambda x: (-x.corrects, x.ended_time))
    return results[offset: offset + 10]
