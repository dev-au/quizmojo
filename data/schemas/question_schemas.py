from pydantic import BaseModel


class QuestionCreateModel(BaseModel):
    text: str
    answer1: str
    answer2: str
    answer3: str
    answer4: str
    correct_answer: int


class QuestionUpdateModel(BaseModel):
    id: int
    text: str
    answer1: str
    answer2: str
    answer3: str
    answer4: str
    correct_answer: int


class AllQuestionsDeleteModel(BaseModel):
    questions: list[int]


class AllQuestionsCreateModel(BaseModel):
    questions: list[QuestionCreateModel]


class AllQuestionsUpdateModel(BaseModel):
    questions: list[QuestionUpdateModel]


class QuestionsGetModel(BaseModel):
    id: int
    text: str
    answer1: str
    answer2: str
    answer3: str
    answer4: str
    correct_answer: int


class QuestionWorkModel(BaseModel):
    id: int
    text: str
    answer1: str
    answer2: str
    answer3: str
    answer4: str
