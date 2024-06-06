from hashlib import sha256
import os
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
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

@router.get("/mask/{file_hash}")
async def get_mask(file_hash: str):
    study = await StudiesDAO.find_one_or_none(file_hash=file_hash)
    if study:
        try:
            with open(study.mask_file_link, 'r') as f:
                data = json.load(f) 
        except Exception as e:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "status_code": "404",
                    "response_type": "error",
                    "description": "Файла с маской ПОКА ЧТО нет",
                    "data": None
                }
            )
        json_string = json.dumps(data)
        json_bytes = json_string.encode('utf-8')
        return {
           "status_code": "200",
           "response_type": "success",
           "description": "Маска отправлена",
           "data": json_bytes
        }
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail= {
        "status_code": "404",
        "response_type": "error",
        "description": "Нет маски для файла с таким хэшом",
        "data": None
        }
    )
    

@router.post("/upload")
async def upload_study(
    current_user: Users = Depends(get_current_user),
    file: UploadFile = File()
):
   if file.filename.endswith('_nii.gz'):
    file_stream = await file.read()
    file_hash = sha256(file_stream).hexdigest() #!

    study_exists = await StudiesDAO.find_one_or_none(file_hash=file_hash)
    if study_exists:
        return {
           "status_code": "200",
           "response_type": "success",
           "description": "Такая маска уже существует, её можно получить по хэшу",
           "data": {
              "file_hash": file_hash
           }
        }

    model_process.delay(
       file_stream=file_stream,
       file_hash=file_hash
    )

    await StudiesDAO.add(
       user_id=current_user.id,
       file_hash=file_hash,
       mask_file_link=os.path.abspath(f'local_data_store/{file_hash}_data.json'),
       study_date=datetime.now()
    )

    return {
        "status_code": "200",
        "response_type": "success",
        "description": "Файл отправлен в модель, он будет готов совсем скоро",
        "data": {
            "file_hash": file_hash
        }
    }

@router.get("/status/{file_hash}")
async def get_status(request: Request, file_hash: str):
    return StreamingResponse(status_generator(file_hash), media_type="text/event-stream")