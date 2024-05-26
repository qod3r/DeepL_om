from fastapi import FastAPI
from app.users.router import router as router_users
from app.studies.router import router as router_studies
from app.main_page.router import router as router_main_page

app = FastAPI()

app.include_router(router_users)
app.include_router(router_studies)
app.include_router(router_main_page)

