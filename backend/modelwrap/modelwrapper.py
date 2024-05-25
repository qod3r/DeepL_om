from pathlib import Path

import numpy as np
from PIL.Image import Image
from torch import Tensor
from ultralytics import YOLO
from ultralytics.engine.results import Results


class ModelWrapper:
    def __init__(self, model_path: Path):
        self.model = YOLO(model_path)

    def predict_one(
        self, image: str | Path | np.ndarray | Image
    ) -> list[Tensor | np.ndarray]:
        results: list[Results] = self.model.predict(image, save=True)

        masks = [result.masks.data for result in results]
        return masks


if __name__ == "__main__":
    model = ModelWrapper(Path("C:/back up/DeepL_om/ml/weights/v8medium_50epoch.pt"))
    print(
        model.predict_one(
            Path("C:/back up/DeepL_om/ml/data/yolo/all_images/study_0509_slice28.png")
        )
    )
