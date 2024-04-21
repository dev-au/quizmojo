from functools import wraps
from time import time

from aioredis import Redis
from fastapi import Request

from data.exceptions import TooManyRequestsException


class RateLimiter:
    redis: Redis

    async def is_rate_limited(self, key: str, limit: int, seconds: int) -> bool:
        current = int(time())
        window_start = current - seconds
        await self.redis.zremrangebyscore(key, 0, window_start)
        count = await self.redis.zcard(key)
        await self.redis.zadd(key, {current: current})
        await self.redis.expire(key, seconds)

        return count > limit

    async def __call__(self, limit: int, seconds: int):
        def decorator(func):
            @wraps(func)
            async def wrapper(request: Request, *args, **kwargs):
                key = f"rate_limit:{request.client.host}:{request.url.path}"
                self.redis = request.app.redis
                if await self.is_rate_limited(key, limit, seconds):
                    raise TooManyRequestsException()
                return await func(request, *args, **kwargs)

            return wrapper

        return decorator
