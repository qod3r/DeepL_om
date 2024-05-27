from fastapi import FastAPI
from app.users.router import router as router_users
from app.study.router import router as router_studies
from app.main_page.router import router as router_main_page
from app.database import init_database

app = FastAPI()

@app.on_event("startup")
async def start_database():
    await init_database()

app.include_router(router_users)
app.include_router(router_studies)
app.include_router(router_main_page)

