from datetime import datetime, timedelta

from data.exceptions import *
from data.models import Quiz
from data.schemas import QuizCreateModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from setup import current_timezone
from urls import quiz_router


@quiz_router.post('', response_model=APIResponse.example_model())
async def create_quiz(user: CurrentUser, quiz_data: QuizCreateModel):
    if 5 < len(quiz_data.name) > 64:
        raise QuizNameValidationException()
    min_length = timedelta(seconds=30)
    max_length = timedelta(hours=24)
    working_time = timedelta(hours=quiz_data.working_time.hour, minutes=quiz_data.working_time.minute,
                             seconds=quiz_data.working_time.second)
    if working_time < min_length or working_time > max_length:
        raise QuizWorkingTimeValidationException()
    if not quiz_data.is_forever:
        current_time = datetime.now(current_timezone)
        quiz_data.starting_time = quiz_data.starting_time.astimezone(current_time)
        quiz_data.ending_time = quiz_data.ending_time.astimezone(current_timezone)
        if quiz_data.starting_time < current_time:
            raise QuizStartingTimeValidationException()
        if quiz_data.ending_time - quiz_data.starting_time < working_time:
            raise QuizEndingTimeValidationException()

    else:
        quiz_data.starting_time = None
        quiz_data.ending_time = None
    await Quiz.create(owner=user, **quiz_data.dict())
    return APIResponse()
