from typing import List, Union

from fastapi.responses import JSONResponse
from pydantic import BaseModel


class APIResponse(JSONResponse):

    def __init__(self, model: Union[BaseModel, List[BaseModel]] = None, **kwargs):
        detail = {
            'status_code': 200,
            'error': None
        }
        response_content = {'detail': detail, 'data': None}

        if isinstance(model, list):
            all_items = []
            for item in model:
                all_items.append(item.dict())
            response_content['data'] = all_items
        elif isinstance(model, BaseModel):
            response_content['data'] = model.dict()
        if kwargs:
            response_content['data'].update(kwargs)
        super().__init__(status_code=200, content=response_content)

    @staticmethod
    def example_model(model: BaseModel = None):
        class ResponseModel(BaseModel):
            detail: dict = {'status_code': 200, 'error': None}
            data: model = None

        return ResponseModel
