#from app.database import users_collection
from bson.objectid import ObjectId
from app.users.models import User
from beanie import Document

users_collection = User

class UsersDAO:
    @classmethod
    async def find_one_or_none(cls, **filtered_by) -> User:
        user = await users_collection.find_one(filtered_by)
        return user
    
    @classmethod
    async def add_user(cls, user: User):
        await user.create()
        