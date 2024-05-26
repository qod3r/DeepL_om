from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=["Main Page"]
)

@router.get("/")
def get_main_page(user):
    pass