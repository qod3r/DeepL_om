from fastapi import Depends, HTTPException, Request, status
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.config import settings
from app.users.dao import UsersDAO

def get_token(request: Request):
    token = request.cookies.get("user_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status_code": 401,
                "response_type": "error",
                "description": "Токен пользователя отсутствует",
                "data": None,
            }
        )
    return token

async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= {
                "status_code": 401,
                "response_type": "error",
                "description": "Неверный формат токена",
                "data": None,
            }
        )
    
    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= {
                "status_code": 401,
                "response_type": "error",
                "description": "Токен пользователя истек",
                "data": None,
            }
        )
    
    user_id: str = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= {
                "status_code": 401,
                "response_type": "error",
                "description": "Пользователь не найден",
                "data": None,
            }
        )
    
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail= {
                "status_code": 401,
                "response_type": "error",
                "description": "Пользователь не найден",
                "data": None,
            }
        )
    return user

