from typing import Optional
from pydantic import BaseModel


class SUserAuth(BaseModel):
    username: str
    password: str


class SUserReg(BaseModel):
    username: str
    lastname: str
    name: str
    patronymic: Optional[str] = None
    post: str
    password: str