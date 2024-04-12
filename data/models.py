from tortoise import Model as DbModel, fields


class User(DbModel):
    username = fields.CharField(pk=True, max_length=16)
    fullname = fields.CharField(max_length=32)
    hashed_password = fields.TextField()


class Quiz(DbModel):
    id = fields.IntField(pk=True)
    owner = fields.ForeignKeyField('models.User')
    name = fields.CharField(max_length=64)
    working_time = fields.TimeField()
    is_private = fields.BooleanField()
    is_forever = fields.BooleanField()
    starting_time = fields.DatetimeField(null=True)
    ending_time = fields.DatetimeField(null=True)


class QuizOption(DbModel):
    id = fields.IntField(pk=True)
    question = fields.TextField()
    answer1 = fields.TextField()
    answer2 = fields.TextField()
    answer3 = fields.TextField()
    answer4 = fields.TextField()
    correct_answer = fields.SmallIntField()
    quiz = fields.ForeignKeyField('models.Quiz')


class ResultQuiz(DbModel):
    user = fields.ForeignKeyField('models.User')
    quiz = fields.ForeignKeyField('models.Quiz')
    corrects = fields.IntField(default=-1)
    started_time = fields.DatetimeField()
    ended_time = fields.DatetimeField(null=True)

    class Meta:
        table = "ResultQuiz"
        unique_together = (("user", "quiz"),)
