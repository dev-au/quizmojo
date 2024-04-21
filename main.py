from aioredis import from_url
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise

from data.exceptions import ERRORS
from setup import *
from urls import ROUTERS
import routes

app = FastAPI(title='QuizMojo',
              description='QuizMojo API',
              version='0.1.0',
              contact={'name': 'dev-au', 'url': 'https://t.me/pycyberuz', 'email': 'devau.business@gmail.com'},
              swagger_ui_parameters={"defaultModelsExpandDepth": -1})
for router in ROUTERS:
    app.include_router(router)


@app.on_event('startup')
async def start_project():
    redis = await from_url(REDIS_URL)
    app.redis = redis
    register_tortoise(
        app,
        db_url=DB_URL,
        modules={'models': ['data.models']},
        generate_schemas=True
    )


@app.get('/errors', include_in_schema=False)
async def project_error_types(request: Request):
    return template.TemplateResponse(request, 'errors.html', {'errors': ERRORS})


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
