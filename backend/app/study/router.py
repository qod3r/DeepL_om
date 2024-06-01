from io import BytesIO
from typing import List
from fastapi import APIRouter, File, UploadFile, BackgroundTasks
import nibabel as nib
from gzip import GzipFile
from modellib.utils.convert import fdata_to_temp_imgs
from modellib.modelwrapper import ModelWrapper
from pathlib import Path
from pprint import pprint
import time
from app.nn_model import model
from app.processing.file_process import get_data_from_nii_file

router = APIRouter(
    prefix="/study",
    tags=["Studies"]
)

@router.get("/mask/{hash}")
def get_mask(hash: str):
    pass

@router.post("/upload")
async def upload_study(
    file: UploadFile = File()
):
    nii_data = await get_data_from_nii_file(file)
    paths = fdata_to_temp_imgs(nii_data, Path('temp/'))
    masks = await model.predict_tempdir_async(paths)
    
    
    

@router.get("/status/{hash}")
def get_status(hash: str):
    pass