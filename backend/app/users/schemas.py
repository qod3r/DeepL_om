from pydantic import BaseModel

class User(BaseModel):
    username: str 
    lastname: str 
    name: str 
    patronymic: str 
    post: str 
    password: str 

    class Config:
        schema_extra = {
            "example": {
                "username": "user1",
                "lastname": "Иванов",
                "name": "Иван",
                "patronymic": "Иванович",
                "post": "Врач",
                "password": "hasshed_password"
            }
        }


