from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["Auth & Users"]
)

@router.get("/info")
def get_user_info(current_user):
    pass

@router.post("/reg")
def register_user(user_data):
    pass

@router.post("/login")
def login_user(response, user_data):
    pass

@router.post("/logout")
def logout_user(response):
    pass