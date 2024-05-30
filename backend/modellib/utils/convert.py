from pathlib import Path
from typing import Literal

import nibabel as nib
import numpy as np
import PIL.Image
from PIL.Image import Image
from skimage.io import imsave
from pydicom import dcmread
from pydicom.data import get_testdata_file
from uuid import uuid4


class Slice:
    def __init__(self, data: Image | np.ndarray, idx: int):
        self.data = data
        self.idx = idx


def study_to_slices(file: Path, type: Literal["nii", "dcm"]) -> list[Slice]:
    data = None
    slices = []

    if type == "nii":
        img = nib.load(file)
        data = img.get_fdata()
    elif type == "dcm":
        path = get_testdata_file(file)
        data = dcmread(path).pixel_array
    if data is None:
        return []

    for slice_idx in range(data.shape[2]):
        slices.append(Slice(data[:, :, slice_idx], idx=slice_idx))

    return slices


def study_to_temp_imgs(
    nii_file: Path,
    save_dir: Path,
    dir_suffix: str = uuid4().hex,
    window_center=-600,
    window_width=1200,
) -> list[Path]: 
    save_dir = save_dir / Path(dir_suffix)
    print(f"save dir: {save_dir}")
    save_dir.mkdir(parents=True, exist_ok=True)
    res: list[Path] = []

    # Load the .nii file
    img = nib.load(str(nii_file))

    # Get the image data
    data = img.get_fdata()

    data = (data - (window_center - window_width / 2)) / window_width * 255
    data = data.clip(0, 255).astype("uint8")

    for slice_idx in range(data.shape[2]):
        out_file = save_dir / f"{nii_file.stem.split('.')[0]}_slice{slice_idx}.png"

        imsave(str(out_file), data[:, :, slice_idx])
        res.append(out_file)
    return res


def clean_temp_dir(dir_path: Path): ...


def normalize_slices(
    slices: list[Slice], window_center=-600, window_width=1200
) -> list[Slice]:
    newslices: list[Slice] = []
    for slice in slices:
        newdata = slice.data

        newdata = (newdata - (window_center - window_width / 2)) / window_width * 255
        newdata = newdata.clip(0, 255).astype("uint8")

        # newimg = PIL.Image.fromarray(newdata).convert("RGB")

        newslices.append(Slice(newdata, slice.idx))

    return slices
