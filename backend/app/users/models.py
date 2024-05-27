from beanie import Document

class User(Document):
    username: str
    lastname: str
    name: str
    patronymic: str
    post: str
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