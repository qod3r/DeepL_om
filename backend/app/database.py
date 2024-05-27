import motor.motor_asyncio
from app.config import settings
from beanie import init_beanie
from app.users.models import User

DATABASE_URI = f"{settings.DB_NAME}://{settings.DB_HOST}:{settings.DB_PORT}"

motor_client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URI)

database = motor_client.studies

users_collection = database.get_collection("users")

async def init_database():
    await init_beanie(
        database=database,
        document_models=[User]
    )
