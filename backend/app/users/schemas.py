from pydantic import BaseModel
from typing import Optional

class UpdateUserSchema(BaseModel):
    username: Optional[str]
    lastname: Optional[str] 
    name: Optional[str] 
    patronymic: Optional[str] 
    post: Optional[str] 
    password: Optional[str]

    class Collection:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "username": "user1",
                "lastname": "Иванов",
                "name": "Иван",
                "patronymic": "Иванович",
                "post": "Врач",
                "password": "hasshed_password"
            }
        }


