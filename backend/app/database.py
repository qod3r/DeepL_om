import motor.motor_asyncio
from app.config import settings
import asyncio

DATABASE_URI = f"{settings.DB_NAME}://{settings.DB_HOST}:{settings.DB_PORT}"

motor_client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

database = motor_client.studies

users_collection = database.get_collection("users")

# async def get_users():
#     async for document in users_collection.find():
#         print(document)


# loop = motor_client.get_io_loop()
# loop.run_until_complete(get_users())
