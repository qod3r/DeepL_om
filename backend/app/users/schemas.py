from pydantic import BaseModel, SecretStr
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

class SUserAuth(BaseModel):
    username: str
    password: str

    class Collection:
        name = "users"

    class Config:
        json_schema_extra = {
            "example": {
                "username": "username",
                "password": "hasshed_password",
            }
        }




