from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

DATABASE_URL = f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"

# Движок для бд
engine = create_async_engine(DATABASE_URL)

# Фабрика сессий бд
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# class for megrations
# Класс, кторый аккумулирует все данные о моделях ORM
class Base(DeclarativeBase):
    pass