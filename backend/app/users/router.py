from fastapi import APIRouter
from app.users.dao import UsersDAO
from app.database import motor_client

router = APIRouter(
    prefix="/user",
    tags=["Auth & Users"]
)

@router.get("/info")
async def get_user_info():
    await UsersDAO.find_by_id()

@router.post("/reg")
async def register_user(username):
    await UsersDAO.add_user(username)

@router.post("/login")
def login_user(response, user_data):
    pass

@router.post("/logout")
def logout_user(response):
    pass