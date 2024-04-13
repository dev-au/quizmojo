from data.exceptions import *
from data.models import Question, Quiz
from data.schemas import AllQuestionsUpdateModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from urls import question_router


@question_router.put('', response_model=APIResponse.example_model())
async def update_questions(user: CurrentUser, questions_data: AllQuestionsUpdateModel):
    first_question = await Question.get_or_none(id=questions_data.questions[0].id)
    if not first_question:
        raise QuestionNotFoundException()
    quiz_id = getattr(first_question, 'quiz_id')
    quiz = await first_question.quiz.get_or_none()
    owner_username = getattr(quiz, 'owner_id')
    if owner_username != user.username:
        raise QuestionNotFoundException()

    for question in questions_data.questions:
        if question.correct_answer not in [1, 2, 3, 4]:
            raise QuestionCorrectAnswerValidationException()
        question_db = await Question.get_or_none(id=question.id)
        if not question_db or getattr(question_db, 'quiz_id') != quiz_id:
            raise QuestionNotFoundException()

        updating_data = question.dict()
        await question_db.update_from_dict(updating_data)
        await question_db.save()
    return APIResponse()
