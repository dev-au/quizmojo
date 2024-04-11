from tortoise import Model as DbModel, fields


class User(DbModel):
    username = fields.CharField(pk=True, max_length=16)
    fullname = fields.CharField(32)
    hashed_password = fields.TextField()


class Quiz(DbModel):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=64)
    owner = fields.ForeignKeyField('models.User')
    is_private = fields.BooleanField()
    working_time = fields.TimeDeltaField()
    starting_time = fields.DatetimeField()
    ending_time = fields.DatetimeField()


class Question(DbModel):
    id = fields.IntField(pk=True)
    quiz = fields.ForeignKeyField('models.Quiz')
    text = fields.TextField()
    answer1 = fields.TextField()
    answer2 = fields.TextField()
    answer3 = fields.TextField()
    answer4 = fields.TextField()
    correct_answer = fields.SmallIntField()


class ResultQuiz(DbModel):
    user = fields.ForeignKeyField('models.User')
    quiz = fields.ForeignKeyField('models.Quiz')
    corrects = fields.IntField()
    time = fields.TimeDeltaField()

    class Meta:
        table = "ResultQuiz"
        unique_together = (("user", "quiz"),)
