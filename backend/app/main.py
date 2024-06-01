from fastapi import FastAPI
from app.users.router import router as router_users
from app.study.router import router as router_studies

app = FastAPI()

app.include_router(router_users)
app.include_router(router_studies)

