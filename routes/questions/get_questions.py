from data.exceptions import *
from data.models import Quiz, Question
from data.schemas import QuestionsGetModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from urls import question_router


@question_router.get('/{quiz_id}', response_model=APIResponse.example_model(list[QuestionsGetModel]))
async def get_questions(user: CurrentUser, quiz_id: int):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    all_questions = await Question.filter(quiz=quiz)
    response = []
    for question in all_questions:
        response.append(QuestionsGetModel(
            id=question.id,
            text=question.text,
            answer1=question.answer1,
            answer2=question.answer2,
            answer3=question.answer3,
            answer4=question.answer4,
            correct_answer=question.correct_answer
        ))
    return APIResponse(response)