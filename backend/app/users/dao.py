# from app.database import users_collection
# from bson.objectid import ObjectId
# from app.users.schemas import User

# class UsersDAO:
#     @classmethod
#     async def find_by_id(cls):
#         async for document in users_collection.find():
#             print(document)

    
#     @classmethod
#     async def add_user(cls, name):
#         document = {
#             "_id": ObjectId(),
#             "name": name
#         }
#         await users_collection.insert_one(document)
#         print("OK")
#         return "zaebisb"

        