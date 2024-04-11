from fastapi.templating import Jinja2Templates

DB_URL = 'sqlite://db.sqlite3'
REDIS_URL = 'redis://localhost:6379/1'

template = Jinja2Templates(directory='templates')
