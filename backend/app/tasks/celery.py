from celery import Celery

from app.config import settings

celery = Celery(
    "tasks",
    broker=settings.BROKER_URL,
    include=["app.tasks.tasks"]
)