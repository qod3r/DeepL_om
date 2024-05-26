from pathlib import Path
import numpy as np
from PIL.Image import Image

class Slice:
    def __init__(self, data: list[str | Path | np.ndarray | Image], idx: int):
        self.data = data
        self.idx = idx


def dicom_to_slices() -> list[Slice]: ...

def normalize(slices: list[Slice], window_center=-600, window_width=1200) -> list[Slice]:
    for slice in slices:
        slice.data = (slice.data - (window_center - window_width / 2)) / window_width * 255
        slice.data = slice.data.clip(0, 255).astype('uint8')
    
    return slices

def dicom_to_numpy(): ...
def nii_to_numpy(): ...