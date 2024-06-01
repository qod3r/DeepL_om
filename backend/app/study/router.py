from hashlib import sha256
import os
from fastapi import APIRouter, Depends, File, Request, UploadFile
import json
from pathlib import Path
import time
from datetime import datetime

from fastapi.responses import StreamingResponse

from app.nn_model import model
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.study.dao import StudiesDAO
from app.tasks.tasks import model_process
from app.study.get_status import status_generator

from modellib.utils.convert import fdata_to_temp_imgs


router = APIRouter(
    prefix="/study",
    tags=["Studies"]
)

@router.get("/mask/{hash}")
def get_mask(hash: str):
    pass

@router.post("/upload")
async def upload_study(
    current_user: Users = Depends(get_current_user),
    file: UploadFile = File()
):
   if file.filename.endswith('_nii.gz'):
    file_stream = await file.read()
    file_hash = sha256(file_stream).hexdigest()

    study_exists = await StudiesDAO.find_one_or_none(file_hash=file_hash)
    if study_exists:
       #TODO: return mask
       return study_exists.mask_file_link
    
    model_process.delay(file_stream)

    return {
       "status": "processed"
    }

    # nii_data = await get_data_from_nii_file(file_data)
    # paths = fdata_to_temp_imgs(nii_data, Path('temp/'))
    # masks = await model.predict_tempdir_async(paths)
    # # end_time = time.time()
    # mask_new = []
    # for mask in masks:
    #      mask_new.append(mask.to_dict())

    # mask_file = {
    #     "file_hash": "hash",
    #     "masks_data": mask_new
    # }

    # with open ('temp_data/data.json', 'w') as f:
    #     json.dump(mask_file, f, indent=4)

    # file_path = os.path.abspath('temp_data/data.json')

    # await StudiesDAO.add(
    #     user_id=current_user.id,
    #     file_hash=file_hash.hexdigest(),
    #     mask_file_link=file_path,
    #     study_date=datetime.now()
    # )
    

    # return {
    #     "status": "ok",
    #     "file_hash": file_hash.hexdigest(),
    #     "user_id": current_user.id,
    #     "file_path": file_path
    # }

@router.get("/status")
async def get_status(request: Request):
    return StreamingResponse(status_generator(), media_type="text/event-stream")