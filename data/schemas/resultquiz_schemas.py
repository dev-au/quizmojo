from datetime import datetime

from pydantic import BaseModel


class ResultQuizModel(BaseModel):
    rank: int
    username: str
    corrects: int
    started_time: datetime
    ended_time: datetime


class ResultsQuizModel(BaseModel):
    results: list[ResultQuizModel]
