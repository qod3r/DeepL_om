from pathlib import Path
from modellib.modelwrapper import ModelWrapper
from app.config import settings

MODEL_PATH = Path(settings.MODEL_PATH)

model = ModelWrapper(MODEL_PATH)




