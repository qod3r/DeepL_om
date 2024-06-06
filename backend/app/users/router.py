from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.users.auth import create_access_token, get_password_hash, authenticate_user
from app.users.dao import UsersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth, SUserReg

router = APIRouter(
    prefix="/user",
    tags=["Auth & Users"]
)

@router.get("/info")
async def get_user_info(current_user: Users = Depends(get_current_user)):
    return current_user

@router.post("/reg")
async def register_user(user_data: SUserReg):
    existing_user = await UsersDAO.find_one_or_none(username=user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={
            "status_code": 409,
            "response_type": "error",
            "description": "Такой пользователь уже существует",
            "data": None,
        })
    hashed_password = get_password_hash(user_data.password)
    user_data.password = hashed_password
    await UsersDAO.add(
        username=user_data.username,
        lastname=user_data.lastname,
        name=user_data.name,
        patronymic=user_data.patronymic,
        post=user_data.post,
        password=hashed_password
    )
    return {
        "status_code": 200,
        "response_type": "success",
        "description": "Пользователь успешно зарегестрирован",
        "data": None,
    }

@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.username, user_data.password)
    if not user:
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