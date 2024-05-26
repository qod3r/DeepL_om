from fastapi import APIRouter

router = APIRouter(
    prefix="/study",
    tags=["Studies"]
)

@router.get("/mask/{hash}")
def get_mask(hash: str):
    pass

@router.post("/upload")
def upload_study(file):
    pass

@router.get("/status/{hash}")
def get_status(hash: str):
    pass