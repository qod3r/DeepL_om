from io import BytesIO
from fastapi import APIRouter, File, UploadFile
import nibabel as nib
from gzip import GzipFile
from modellib.utils.convert import study_to_temp_imgs
from modellib.modelwrapper import ModelWrapper
from pathlib import Path
from pprint import pprint
import time
from app.nn_model import model

router = APIRouter(
    prefix="/study",
    tags=["Studies"]
)

@router.get("/mask/{hash}")
def get_mask(hash: str):
    pass

@router.post("/upload")
async def upload_study(
    # file: UploadFile = File()
):
    # start_time = time.time()
    # compressed_data = await file.read()
    # compressed_stream = BytesIO(compressed_data)
    # with GzipFile(
    #     fileobj=compressed_stream, mode='rb'
    # ) as decompressed_stream:
    #     nifti_data = BytesIO(decompressed_stream.read())
    # compressed_stream.close()
    # nifti_image = nib.nifti1.Nifti1Image.from_bytes(nifti_data.read())
    # data = nifti_image.get_fdata()
    
    # print(file.filename[:-7])

    # paths = study_to_temp_imgs(file_name=file.filename[:-7], data=data, save_dir=Path('temp/'))
    # model = ModelWrapper(Path('C:/Users/HYPERPC/Code/diploma/DeepL_om/ml/weights/v8medium_50epoch.pt'))

    # masks = model.predict_tempdir(paths)
    # pprint([(mask.slice_idx, mask.data.shape) for mask in masks])
    # end_time = time.time()
    # return {
    #     "time": end_time - start_time
    # }

    pass
    

@router.get("/status/{hash}")
def get_status(hash: str):
    pass