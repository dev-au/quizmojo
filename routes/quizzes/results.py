import io

import pandas as pd
from fastapi import Response

from data.exceptions import *
from data.models import Quiz, ResultQuiz
from data.schemas import ResultQuizModel, ResultsQuizModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from urls import quiz_router


@quiz_router.get('/results', response_model=APIResponse.example_model(ResultsQuizModel))
async def result_quizzes(user: CurrentUser, quiz_id: int, page: int):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    await ResultQuiz.finish_latecomers(quiz_id)
    results = await ResultQuiz.filter(quiz=quiz, corrects__ne=-1)
    offset = (page - 1) * 10
    if quiz.is_forever:
        results = sorted(results, key=lambda x: (-x.corrects, x.ended_time - x.started_time))
    else:
        results = sorted(results, key=lambda x: (-x.corrects, x.ended_time))
    results_quiz = []
    sorted_results = results[offset: offset + 10]
    for result in sorted_results:
        results_quiz.append(
            ResultQuizModel(username=getattr(result, 'user_id'), quiz_id=quiz.id, corrects=result.corrects,
                            started_time=result.started_time, ended_time=result.ended_time))

    return ResultsQuizModel(results=results_quiz)


@quiz_router.get('/results-excel', response_class=Response)
async def result_quizzes_excel(user: CurrentUser, quiz_id: int):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    await ResultQuiz.finish_latecomers(quiz_id)
    results = await ResultQuiz.filter(quiz=quiz, corrects__ne=-1)
    data = []
    for result in results:
        data.append({
            "User": result.user.username,
            "Corrects": result.corrects,
            "Started Time": result.started_time,
            "Ended Time": result.ended_time
        })
    df = pd.DataFrame(data)
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    return Response(
        excel_file.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment;filename=results.xlsx"}
    )
