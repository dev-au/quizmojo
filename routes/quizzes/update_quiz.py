from datetime import datetime, timedelta

from data.exceptions import *
from data.models import Quiz
from data.schemas import QuizCreateModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from setup import timezone
from urls import quiz_router


@quiz_router.put('/{quiz_id}', response_model=APIResponse.example_model())
async def update_quiz_option(user: CurrentUser, quiz_id: int, quiz_data: QuizCreateModel):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    if 5 < len(quiz_data.name) > 64:
        raise QuizNameValidationException()
    min_length = timedelta(seconds=30)
    max_length = timedelta(hours=24)
    working_time = timedelta(hours=quiz_data.working_time.hour, minutes=quiz_data.working_time.minute,
                             seconds=quiz_data.working_time.second)
    if working_time < min_length or working_time > max_length:
        raise QuizWorkingTimeValidationException()
    if not quiz_data.is_forever:
        current_time = datetime.now(timezone)
        quiz_data.starting_time = quiz_data.starting_time.astimezone(timezone)
        quiz_data.ending_time = quiz_data.ending_time.astimezone(timezone)
        if quiz_data.starting_time < current_time:
            raise QuizStartingTimeValidationException()
        if quiz_data.ending_time - quiz_data.starting_time < working_time:
            raise QuizEndingTimeValidationException()

    else:
        quiz_data.starting_time = None
        quiz_data.ending_time = None
    await quiz.update_from_dict(quiz_data.dict())
    await quiz.save()
    return APIResponse()
