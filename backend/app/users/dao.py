from app.database import users_collection
from bson.objectid import ObjectId
from app.database import motor_client
import asyncio

class UsersDAO:
    @classmethod
    async def find_by_id(cls, user_id: int):
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return user
        