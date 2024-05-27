from beanie import Document
from bson import ObjectId
from typing import Optional

class User(Document):
    _id: ObjectId
    username: str
    lastname: Optional[str] = None
    name: Optional[str] = None
    patronymic: Optional[str] = None
    post: Optional[str] = None
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "username",
                "lastname": "Иванов",
                "name": "Иван",
                "patronymic": "Иванович",
                "post": "Врач",
                "password": "hashed-password"
            }
        }

    class Settings:
        name = "users"