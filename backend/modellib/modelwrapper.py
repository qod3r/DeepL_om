from pathlib import Path
from typing import Self

from utils import Slice
import numpy as np

from torch import Tensor
from ultralytics import YOLO
from ultralytics.engine.results import Results


# data for one slice
class Mask:
    def __init__(self, data: Tensor | np.ndarray, slice_idx: int | None = None):
        self.data = data
        self.slice_idx = slice_idx

    def as_tuple(self):
        return (self.slice_idx, self.data)

    def __add__(self, other: Self):
        return self.data + other.data

    # for sum()
    def __radd__(self, other: Self):
        try:
            return self.data + other.data
        except:
            return self


# data for entire study
class MaskBundle:
    def __init__(self, data): ...


class ModelWrapper:
    def __init__(self, model_path: Path):
        self.model = YOLO(model_path)

    def predict(self, slices: list[Slice]) -> list[list[Mask]]:
        res = []
        for slice in slices:
            results: list[Results] = self.model.predict(slice)

            masks: list[Mask] = []
            for idx, result in enumerate(results):
                for mask in result.masks.data:
                    masks.append(Mask(data=mask, slice_idx=idx))

            res.append(masks)
        return res


if __name__ == "__main__":
    model = ModelWrapper(Path("C:/back up/DeepL_om/ml/weights/v8medium_50epoch.pt"))
    studies = [
        Path("C:/back up/DeepL_om/ml/data/yolo/all_images/study_0509_slice28.png"),
        Path("C:/back up/DeepL_om/ml/data/yolo/all_images/study_0509_slice29.png"),
        Path("C:/back up/DeepL_om/ml/data/yolo/all_images/study_0509_slice30.png"),
        Path("C:/back up/DeepL_om/ml/data/yolo/all_images/study_0509_slice31.png"),
    ]
    masks = model.predict(studies)
    for study in masks:
        for mask in study:
            print(f"{mask.slice_idx} {(mask.data)}")
    
    print(sum(sum(sum(masks[0]))))
