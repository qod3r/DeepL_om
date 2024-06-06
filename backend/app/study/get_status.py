import asyncio
from fastapi import HTTPException, status
from redis import Redis

redis = Redis()

async def status_generator(file_hash: str):
    status = ''
    while status != b'done':
        status = redis.get(f'{file_hash}_status')
        # print(f"STATUS\tvalue:{status}\ttype:{type(status)}")
        yield status
        await asyncio.sleep(1)
    #redis.delete(f'{file_hash}_status')
    redis.flushall()