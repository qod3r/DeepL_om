from pathlib import Path

from modellib import ModelWrapper
from modellib.utils import dicom_to_slices


if __name__ == "__main__":
    model = ModelWrapper(Path("path/to/model.pt"))
    
    dicom_file = Path("path/to/study.dcm")
    slices = dicom_to_slices(dicom_file)

    result = model.predict(slices)
