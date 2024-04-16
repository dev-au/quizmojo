import pytz
from fastapi.templating import Jinja2Templates

current_timezone = pytz.timezone('Asia/Tashkent')

DB_URL = 'sqlite://db.sqlite3'
REDIS_URL = 'redis://localhost:6379/1'

template = Jinja2Templates(directory='templates')

SECRET_KEY = "1aa7c3c8c5563fb00439b132eb711fe26a36e74b267aa030bbd347fbf2695825"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30
