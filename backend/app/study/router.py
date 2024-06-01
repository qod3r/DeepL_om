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
from app.study.get_mask import send_mask

from modellib.utils.convert import fdata_to_temp_imgs


router = APIRouter(
    prefix="/study",
    tags=["Studies"]
)

@router.get("/mask/{hash}")
async def get_mask(hash: str):
    study = await StudiesDAO.find_one_or_none(file_hash=hash)
    if study:
        with open(f'temp_data/study_0255_data.json', 'r') as f:
            data = json.load(f)
        json_string = json.dumps(data)
        json_bytes = json_string.encode('utf-8')
        return {
           "data": json_bytes
        }
    

@router.post("/upload")
async def upload_study(
    current_user: Users = Depends(get_current_user),
    file: UploadFile = File()
):
   if file.filename.endswith('_nii.gz'):
    file_stream = await file.read()
    file_hash = sha256().hexdigest()

    study_exists = await StudiesDAO.find_one_or_none(file_hash=file_hash)
    if study_exists:
       #TODO: return mask
        return {
           "status": "exists"
        }

    
    model_process.delay(file_stream, file_name=file.filename[:-7])

    return {
       "status": "processed"
    }

@router.get("/status/{file_name}")
async def get_status(request: Request, file_name: str):
    return StreamingResponse(status_generator(file_name), media_type="text/event-stream")