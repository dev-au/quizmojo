from datetime import datetime, timedelta, time

from tortoise import Model, fields

from data.exceptions import QuizNotFoundException
from setup import current_timezone


class User(Model):
    username = fields.CharField(pk=True, max_length=16)
    phone = fields.IntField()
    fullname = fields.CharField(max_length=32)
    hashed_password = fields.TextField()


class Quiz(Model):
    id = fields.IntField(pk=True)
    owner = fields.ForeignKeyField('models.User')
    name = fields.CharField(max_length=64)
    working_time: time = fields.TimeField()
    is_private = fields.BooleanField()
    is_forever = fields.BooleanField()
    is_active = fields.BooleanField()
    starting_time = fields.DatetimeField(null=True)
    ending_time = fields.DatetimeField(null=True)

    @property
    def has_expired(self):
        if not self.is_forever:
            if self.ending_time <= datetime.now(current_timezone):
                return True
            elif self.starting_time + timedelta(
                    hours=self.working_time.hour,
                    minutes=self.working_time.minute,
                    seconds=self.working_time.second,
            ) < self.ending_time:
                return True
        return False


class Question(Model):
    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=255)
    answer1 = fields.CharField(max_length=100)
    answer2 = fields.CharField(max_length=100)
    answer3 = fields.CharField(max_length=100)
    answer4 = fields.CharField(max_length=100)
    correct_answer = fields.SmallIntField()
    quiz = fields.ForeignKeyField('models.Quiz')


class ResultQuiz(Model):
    user = fields.ForeignKeyField('models.User')
    quiz = fields.ForeignKeyField('models.Quiz')
    corrects = fields.IntField(default=-1)
    started_time = fields.DatetimeField(default=datetime.now(current_timezone))
    ended_time = fields.DatetimeField(null=True)

    class Meta:
        unique_together = (("user", "quiz"),)

    @staticmethod
    async def finish_latecomers(quiz_id: int):
        quiz = await Quiz.get_or_none(id=quiz_id)
        if not quiz:
            raise QuizNotFoundException()
        results = await ResultQuiz.filter(quiz=quiz)
        for result in results:
            if result.corrects == -1:
                max_time_limit = result.started_time + timedelta(hours=quiz.working_time.hour,
                                                                 minutes=quiz.working_time.minute,
                                                                 seconds=quiz.working_time.second)
                if max_time_limit >= datetime.now(current_timezone):
                    result.corrects = 0
                    result.ended_time = max_time_limit
                    await result.save()


class UserAcceptQuiz(Model):
    user = fields.ForeignKeyField('models.User')
    quiz = fields.ForeignKeyField('models.Quiz')
