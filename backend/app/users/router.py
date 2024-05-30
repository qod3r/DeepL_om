from fastapi import APIRouter, Depends, Response
from app.users.dao import UsersDAO
from app.database import motor_client
from bson.json_util import dumps

from app.users.dependencies import get_current_user
from app.users.schemas import SUserAuth
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from fastapi import HTTPException, status
from app.users.models import User

router = APIRouter(
    prefix="/user",
    tags=["Auth & Users"]
)

@router.get("/info")
async def get_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/reg")
async def register_user(user_data: User):
    existing_user = await UsersDAO.find_one_or_none(username=user_data.username)
    print(existing_user)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "status_code": 409,
            "response_type": "error",
            "description": "Такой пользователь уже существует",
            "data": None,
        })
    hashed_password = get_password_hash(user_data.password)
    user_data.password = hashed_password
    await UsersDAO.add_user(user_data)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Пользователь успешно зарегестрирован",
        "data": None,
    }

@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.username, user_data.password)
    if user == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={
            "status_code": 401,
            "response_type": "error",
            "description": "Неверный логин или пароль",
            "data": None,
        })
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("user_access_token", access_token, httponly=True)
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Вход выполнен успешно",
        "data": {
            "user_access_token": access_token,
        },
    }

@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("user_access_token")
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Выход выполнен успешно",
        "data": None,

    }