import io

import pandas as pd
from fastapi import Response

from data.exceptions import *
from data.models import Quiz, ResultQuiz
from data.schemas import ResultQuizModel, ResultsQuizModel
from resources.api_response import APIResponse
from resources.depends import CurrentUser
from resources.error_docs import error_docs
from urls import quiz_router


@error_docs(QuizNotFoundException)
@quiz_router.get('/results/{quiz_id}', response_model=APIResponse.example_model(ResultsQuizModel))
async def result_quizzes(user: CurrentUser, quiz_id: int, page: int):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    await ResultQuiz.finish_latecomers(quiz_id)
    all_results = await ResultQuiz.filter(quiz=quiz)
    filtered_results = [result for result in all_results if result.corrects != -1]
    offset = (page - 1) * 10
    if quiz.is_forever:
        results = sorted(filtered_results, key=lambda x: (-x.corrects, x.ended_time - x.started_time))
    else:
        results = sorted(filtered_results, key=lambda x: (-x.corrects, x.ended_time))
    results_quiz = []
    sorted_results = results[offset: offset + 10]
    rank = 1
    for result in sorted_results:
        results_quiz.append(
            ResultQuizModel(rank=rank, username=getattr(result, 'user_id'), corrects=result.corrects,
                            started_time=result.started_time, ended_time=result.ended_time))
        rank += 1

    return APIResponse(ResultsQuizModel(results=results_quiz))


@error_docs(QuizNotFoundException)
@quiz_router.get('/results-excel/{quiz_id}', response_class=Response)
async def result_quizzes_excel(user: CurrentUser, quiz_id: int):
    quiz = await Quiz.get_or_none(id=quiz_id, owner=user)
    if not quiz:
        raise QuizNotFoundException()
    await ResultQuiz.finish_latecomers(quiz_id)
    all_results = await ResultQuiz.filter(quiz=quiz)
    filtered_results = [result for result in all_results if result.corrects != -1]
    data = []
    if quiz.is_forever:
        results = sorted(filtered_results, key=lambda x: (-x.corrects, x.ended_time - x.started_time))
    else:
        results = sorted(filtered_results, key=lambda x: (-x.corrects, x.ended_time))
    rank = 1
    for result in results:
        data.append({
            "Rank": rank,
            "User": getattr(result, 'user_id'),
            "Corrects": result.corrects,
            "Started Time": str(result.started_time),
            "Ended Time": str(result.ended_time)
        })
        rank += 1
    df = pd.DataFrame(data)
    excel_file = io.BytesIO()
    df.to_excel(excel_file, index=False)
    excel_file.seek(0)
    return Response(
        excel_file.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment;filename=results.xlsx"}
    )
