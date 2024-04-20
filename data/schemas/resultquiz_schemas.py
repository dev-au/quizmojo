from datetime import datetime

from pydantic import BaseModel


class ResultQuizModel(BaseModel):
    username: str
    quiz_id: int
    corrects: int
    started_time: datetime
    ended_time: datetime


class ResultsQuizModel(BaseModel):
    results: list[ResultQuizModel]
