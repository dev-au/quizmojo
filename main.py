from aioredis import from_url
from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    key = f"rate_limit:{request.client.host}:{request.url.path}"
    redis = request.app.redis
    current_count = await redis.incr(key, 1)
    if current_count == 1:
        await redis.expire(key, 60)
    elif current_count > 20:
        return JSONResponse({'detail': {'status_code': 429, 'error': 'TooManyRequestsException'}}, 429)
    response = await call_next(request)
    return response


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
