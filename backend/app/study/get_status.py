import asyncio
from fastapi import HTTPException, status
from redis import Redis

redis = Redis()

async def status_generator(file_name: str):
    status = ''
    while status != 'done':
        yield redis.get(f'{file_name}_status')
        await asyncio.sleep(1)
    redis.delete(f'{file_name}_status')