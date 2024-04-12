import json

from fastapi import status, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel


class APIResponse(JSONResponse):

    def __init__(self, model: BaseModel, **kwargs):
        detail = {
            'status_code': 200,
            'error': None
        }
        response_content = {'detail': detail, 'data': model.dict()}
        if kwargs:
            response_content['data'].update(kwargs)
        super().__init__(status_code=200, content=response_content)

    @staticmethod
    def example_model(model: BaseModel):
        class ResponseModel(BaseModel):
            detail: dict = {'status_code': 200, 'error': None}
            data: model

        return ResponseModel
