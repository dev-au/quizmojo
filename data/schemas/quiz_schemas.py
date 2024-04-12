from datetime import timedelta, datetime, time

from pydantic import BaseModel


class QuizCreateModel(BaseModel):
    name: str
    is_private: bool
    working_time: time
    is_forever: bool
    starting_time: datetime
    ending_time: datetime


class QuizInfoModel(BaseModel):
    id: int
    name: str
    is_private: bool
    working_time: str
    is_forever: bool
    starting_time: str | None
    ending_time: str | None
