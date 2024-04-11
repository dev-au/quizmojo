from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from tortoise.contrib.fastapi import register_tortoise
from aioredis import from_url
from setup import *
from urls import ROUTERS
import routes

app = FastAPI(title='Iqtidor IT Quiz', swagger_ui_parameters={"defaultModelsExpandDepth": -1})
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


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)