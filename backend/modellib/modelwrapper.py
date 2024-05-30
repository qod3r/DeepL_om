from pathlib import Path
from typing import Self

import numpy as np
import PIL.Image
from torch import Tensor
from ultralytics import YOLO
from ultralytics.engine.results import Results
from utils import Slice

from uuid import uuid4

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
        self.progress: float = 0
        self.is_processing: bool = False

    def predict(self, slices: list[Slice]) -> list[list[Mask]]:
        pred = []
        
        self.is_processing = True
        for idx, slice in enumerate(slices):
            self.progress = idx / len(slices)
            if isinstance(slice, Path):
                results: list[Results] = self.model.predict(slice)
            else:
                slice.data = PIL.Image.fromarray(slice.data).convert("RGB")
                print(f"Slice {slice.idx}:")
                results: list[Results] = self.model.predict(slice.data)
            
            for ridx, result in enumerate(results):
                if len(result):
                    print(f"\t{ridx=} {len(result)=}")
                    for midx, mask in enumerate(result.masks.data):
                        print(f"\t\t{midx=} {sum(sum(mask))=}")
                        # masks.append(Mask(data=mask, slice_idx=idx))
        
        
        self.is_processing = False
        self.progress = 0
        return pred

    def predict_tempdir(self, slices: list[Path], combine_masks: bool = True) -> list[Mask]:
        pred = []
        
        self.is_processing = True
        for idx, slice in enumerate(slices):
            self.progress = idx / len(slices)
            results: list[Results] = self.model.predict(slice)
            
            # skip 0 detections
            if not len(results[0]):
                continue
            
            combined: list[Tensor | np.ndarray] = []
            separate: list[Mask] = []
            
            for midx, mask in enumerate(results[0].masks.data):
                combined.append(mask)
                separate.append(Mask(data=mask, slice_idx=idx))
        
            # combine all slice masks into one
            combined = sum(combined)
            combined_mask = Mask(data=combined, slice_idx=idx)
        
            if combine_masks:
                pred.append(combined_mask)
            else:
                pred.extend(separate)
            
        self.is_processing = False
        self.progress = 0
        return pred

if __name__ == "__main__":
    from utils import study_to_temp_imgs
    from pprint import pprint
    
    TEMP_DIR = Path("temp/")
    
    
    model = ModelWrapper(Path("C:/back up/DeepL_om/ml/weights/v8medium_50epoch.pt"))

    nii_study = Path("study_0509.nii.gz")
    nii_imgs = study_to_temp_imgs(nii_study, TEMP_DIR)
    
    masks = model.predict_tempdir(nii_imgs)
    
    pprint([(mask.slice_idx, mask.data.shape) for mask in masks])

