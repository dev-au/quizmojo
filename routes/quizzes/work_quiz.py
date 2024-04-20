from datetime import datetime

from data.exceptions import *
from data.models import Quiz, ResultQuiz, Question, UserAcceptQuiz
from data.schemas import QuizWorkModel, QuestionWorkModel, QuestionsAnswerModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from setup import current_timezone
from urls import quiz_router


@quiz_router.get('/work/{quiz_id}', response_model=APIResponse.example_model(QuizWorkModel))
async def user_get_working_quiz(user: CurrentUser, quiz_id: int):
    quiz = await Quiz.get_or_none(id=quiz_id)
    if not quiz:
        raise QuizNotFoundException()
    result_quiz = await ResultQuiz.get_or_none(user=user, quiz=quiz)
    if result_quiz:
        if result_quiz.corrects == -1:
            raise QuizIsNowWorkingException()
        else:
            raise QuizAlreadyWorkedException()

    if not quiz.is_active or quiz.has_expired:
        raise QuizExpiredException()
    if quiz.is_private:
        is_accepted = await UserAcceptQuiz.get_or_none(user=user, quiz=quiz)
        if not is_accepted:
            raise QuizAccessException()

    await ResultQuiz.create(user=user, quiz=quiz)
    questions = []
    all_questions = await Question.filter(quiz=quiz)
    for question in all_questions:
        questions.append(
            QuestionWorkModel(
                id=question.id,
                text=question.text,
                answer1=question.answer1,
                answer2=question.answer2,
                answer3=question.answer3,
                answer4=question.answer4
            )
        )
    return APIResponse(QuizWorkModel(
        quiz_id=quiz.id,
        quiz_name=quiz.name,
        working_time=str(quiz.working_time),
        questions=questions
    ))


@quiz_router.post('/work/{quiz_id}', response_model=APIResponse.example_model())
async def user_work_quiz(user: CurrentUser, quiz_id: int, answers: QuestionsAnswerModel):
    quiz = await Quiz.get_or_none(id=quiz_id)
    if not quiz:
        raise QuizNotFoundException()
    result_quiz = await ResultQuiz.get_or_none(user=user, quiz=quiz)
    if not result_quiz:
        raise UserNotRegisteredException()
    if result_quiz.corrects != -1:
        raise QuizAlreadyWorkedException()

    if not quiz.is_active or quiz.has_expired:
        raise QuizExpiredException()
    if quiz.is_private:
        is_accepted = await UserAcceptQuiz.get_or_none(user=user, quiz=quiz)
        if not is_accepted:
            raise QuizAccessException()
    user_answers = {}
    for answer in answers.answers:
        user_answers[answer.id] = answer.correct_answer
    correct_answers = 0
    all_questions = await Question.filter(quiz=quiz)
    for question in all_questions:
        try:
            if question.correct_answer == user_answers[question.id]:
                correct_answers += 1
        except KeyError:
            pass
    result_quiz.corrects = correct_answers
    result_quiz.ended_time = datetime.now(current_timezone)
    await result_quiz.save()
