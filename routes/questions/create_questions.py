from data.exceptions import *
from data.models import Quiz, Question
from data.schemas import AllQuestionsCreateModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from resources.error_docs import error_docs
from urls import question_router


@error_docs(QuizNotFoundException, QuestionCorrectAnswerValidationException)
@question_router.post('', response_model=APIResponse.example_model())
async def create_questions(user: CurrentUser, quiz_id: int, questions_data: AllQuestionsCreateModel):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    for question in questions_data.questions:
        if question.correct_answer not in [1, 2, 3, 4]:
            raise QuestionCorrectAnswerValidationException()
        question_data = question.dict()
        await Question.create(**question_data, quiz=quiz)
    return APIResponse()
