from datetime import datetime, timedelta, time

from tortoise import Model, fields

from setup import current_timezone


class User(Model):
    username = fields.CharField(pk=True, max_length=16)
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
                    seconds=self.working_time.second + 10
            ) < self.ending_time:
                return True
        return False


class Question(Model):
    id = fields.IntField(pk=True)
    text = fields.TextField()
    answer1 = fields.TextField()
    answer2 = fields.TextField()
    answer3 = fields.TextField()
    answer4 = fields.TextField()
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


class JoiningRequest(Model):
    user = fields.ForeignKeyField('models.User')
    quiz = fields.ForeignKeyField('models.Quiz')
    is_accepted = fields.BooleanField(default=False)
