from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.users.router import router as router_users
from app.study.router import router as router_studies

app = FastAPI()

app.include_router(router_users)
app.include_router(router_studies)

# origins = [
#     "http://localhost:8000", #Вместо 8000 указываешь порт на котором React 5173
#     "http://127.0.0.1:8000",
#     "http://0.0.0.0:8000"
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=True,
#     allow_credential=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )