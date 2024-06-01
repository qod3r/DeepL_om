from pathlib import Path
from typing import List

from app.tasks.celery import celery
from app.nn_model import model

@celery.task
def model_process(
    paths: List[Path]
):
    masks = model.predict_tempdir(paths)
    