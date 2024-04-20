from data.exceptions import *
from data.models import Quiz
from data.schemas import QuizInfoModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from urls import quiz_router


@quiz_router.get('', response_model=APIResponse.example_model(list[QuizInfoModel]))
async def get_all_quizzes(user: CurrentUser, page: int):
    response = []
    offset = (page - 1) * 10
    all_quizzes = await Quiz.filter(owner=user).offset(offset).limit(10)

    for quiz in all_quizzes:
        if not quiz.is_forever:
            quiz.starting_time = str(quiz.starting_time)
            quiz.ending_time = str(quiz.ending_time)
        response.append(QuizInfoModel(
            id=quiz.id,
            name=quiz.name,
            working_time=str(quiz.working_time),
            is_private=quiz.is_private,
            is_forever=quiz.is_forever,
            is_active=quiz.is_active,
            starting_time=quiz.starting_time,
            ending_time=quiz.ending_time
        ))
    return APIResponse(response)


@quiz_router.get('/{quiz_id}', response_model=APIResponse.example_model(QuizInfoModel))
async def get_one_quiz(user: CurrentUser, quiz_id: int):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    if not quiz.is_forever:
        quiz.starting_time = str(quiz.starting_time)
        quiz.ending_time = str(quiz.ending_time)
    return APIResponse(QuizInfoModel(
        id=quiz.id,
        name=quiz.name,
        working_time=str(quiz.working_time),
        is_private=quiz.is_private,
        is_forever=quiz.is_forever,
        is_active=quiz.is_active,
        starting_time=quiz.starting_time,
        ending_time=quiz.ending_time
    ))
