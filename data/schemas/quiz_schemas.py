from datetime import datetime, time

from pydantic import BaseModel

from .question_schemas import QuestionWorkModel


class QuizGetModel(BaseModel):
    id: int


class QuizCreateModel(BaseModel):
    name: str
    working_time: time
    is_private: bool
    is_forever: bool
    is_active: bool
    starting_time: datetime
    ending_time: datetime


class QuizInfoModel(BaseModel):
    id: int
    name: str
    working_time: str
    is_private: bool
    is_forever: bool
    is_active: bool
    starting_time: str | None
    ending_time: str | None


class QuizWorkModel(BaseModel):
    quiz_id: int
    quiz_name: str
    working_time: time
    questions: list[QuestionWorkModel]

