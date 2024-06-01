import asyncio
from redis import Redis

redis = Redis()

async def status_generator():
    status = ''
    while status != 'done':
        yield redis.get('processing')
        await asyncio.sleep(1)