from data.exceptions import *
from data.models import Question
from data.schemas import AllQuestionsDeleteModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from resources.error_docs import error_docs
from urls import question_router


@error_docs(QuestionNotFoundException)
@question_router.delete('', response_model=APIResponse.example_model())
async def delete_questions(user: CurrentUser, questions_data: AllQuestionsDeleteModel):
    first_question = await Question.get_or_none(id=questions_data.questions[0])
    if not first_question:
        raise QuestionNotFoundException()
    quiz_id = getattr(first_question, 'quiz_id')
    quiz = await first_question.quiz.get_or_none()
    owner_username = getattr(quiz, 'owner_id')
    if owner_username != user.username:
        raise QuestionNotFoundException()

    for question in questions_data.questions:
        question_db = await Question.get_or_none(id=question)
        if not question_db or getattr(question_db, 'quiz_id') != quiz_id:
            raise QuestionNotFoundException()
        await question_db.delete()
    return APIResponse()
