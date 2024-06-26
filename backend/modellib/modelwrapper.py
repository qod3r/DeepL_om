import asyncio
from pathlib import Path
from typing import Self
from uuid import uuid4

import numpy as np
import PIL.Image
from skimage.transform import resize
from torch import Tensor
from ultralytics import YOLO
from ultralytics.engine.results import Results
from modellib.utils.convert import Slice

import asyncio
from uuid import uuid4


# data for one slice
class Mask:
    def __init__(self, data: Tensor | np.ndarray, slice_idx: int | None = None):
        self.data = data
        self.slice_idx = slice_idx

    def as_tuple(self):
        return (self.slice_idx, self.data)
    
    def resize(self, dims: tuple[int, int]) -> Self:
        """Returns a resized copy of itself"""
        
        if dims is None:
            return self
        
        return Mask(resize(self.data.numpy(), dims), self.slice_idx)
        

    def __add__(self, other: Self):
        return self.data + other.data

    # for sum()
    def __radd__(self, other: Self):
        try:
            return self.data + other.data
        except:
            return self
        
    def to_dict(self):
        return {
            "data": self.data.tolist(),
            "slice_idx": self.slice_idx
        }
        


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

    def predict_tempdir(
        self, slices: list[Path], combine_masks: bool = True
    ) -> list[Mask]:
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

    async def predict_tempdir_async(
        self, slices: list[Path], combine_masks: bool = True
    ) -> list[Mask]:
        pred = []
        self.is_processing = True

        tasks = [self._predict_slice_tempdir(slice, idx) for idx, slice in enumerate(slices)]
        results = await asyncio.gather(*tasks)

        for idx, (slice_results, slice_idx) in enumerate(results):
            self.progress = idx / len(slices)

            if not len(slice_results[0]):
                continue

            combined: list[Tensor | np.ndarray] = []
            separate: list[Mask] = []

            for midx, mask in enumerate(slice_results[0].masks.data):
                combined.append(mask)
                separate.append(Mask(data=mask, slice_idx=slice_idx))

            combined = sum(combined)
            combined_mask = Mask(data=combined, slice_idx=slice_idx)

            if combine_masks:
                pred.append(combined_mask)
            else:
                pred.extend(separate)

        self.is_processing = False
        self.progress = 0
        return pred

    async def _predict_slice_tempdir(
        self, slice: Path, slice_idx: int
    ) -> tuple[list[Results], int]:
        results = self.model.predict(slice)
        return results, slice_idx


if __name__ == "__main__":
    from modellib.utils.convert import study_to_temp_imgs, fdata_to_temp_imgs
    from pprint import pprint

    from utils import fdata_to_temp_imgs, study_to_temp_imgs

    # папка для распаковки исследования, 1 раз
    TEMP_DIR = Path("temp/")

    # init модели, 1 раз
    model = ModelWrapper(Path("C:/back up/DeepL_om/ml/weights/v8medium_50epoch.pt"))

    # а это при каждом запросе
    nii_study = Path("study_0509.nii.gz")
    nii_imgs = study_to_temp_imgs(nii_study, TEMP_DIR)
    masks = model.predict_tempdir(nii_imgs)
    # или
    #   nii_study = <nib>.get_fdata()
    #   nii_imgs = fdata_to_temp_imgs(nii_study, TEMP_DIR)
    #   masks = await model.predict_tempdir_async(nii_imgs)


    pprint(masks[0].data.shape)
    pprint(masks[0].resize((512, 512)).data.shape)
        
    # async def run_prediction():
    #     start_time = time.time()
    #     masks = await model.predict_tempdir_async(nii_imgs, combine_masks=True)
    #     end_time = time.time()
    #     print(f"Prediction took {end_time - start_time:.2f} seconds")
    #     print(f"Number of masks: {len(masks)}")

    # asyncio.run(run_prediction())

    pprint([(mask.slice_idx, mask.data.shape) for mask in masks])
    # -----------------------------------
