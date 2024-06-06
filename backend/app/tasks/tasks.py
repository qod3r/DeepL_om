from gzip import GzipFile
from io import BytesIO
import json
from pathlib import Path
from typing import List
import nibabel as nib
from redis import Redis

from app.tasks.celery import celery
from app.nn_model import model
from app.study.dao import StudiesDAO
from modellib.utils.convert import fdata_to_temp_imgs


redis = Redis()

@celery.task
def model_process(
    file_stream: bytes,
    file_name: str,
):
    redis.set(f'{file_name}_status', 'pending')
    compressed_stream = BytesIO(file_stream)
    with GzipFile(
        fileobj=compressed_stream, mode='rb'
    ) as decompressed_stream:
        nifti_data = BytesIO(decompressed_stream.read())
    compressed_stream.close()
    nifti_image = nib.nifti1.Nifti1Image.from_bytes(nifti_data.read())
    data = nifti_image.get_fdata()
    redis.set(f'{file_name}_status', 'file_read')
    paths = fdata_to_temp_imgs(data, Path('temp/'))
    redis.set(f'{file_name}_status', 'sent to model')
    masks = model.predict_tempdir(paths)
    redis.set(f'{file_name}_status', 'got result from model')
    dicted_masks = []
    for mask in masks:
        dicted_masks.append(mask.to_dict())
    redis.set(f'{file_name}_status', 'masks are ready')
    mask_file = {
        "file_hash": "hash",
        "masks_data": dicted_masks
    }
    redis.set(f'{file_name}_status', 'writing json')
    with open (f'temp_data/{file_name}_data.json', 'w') as f:
        json.dump(mask_file, f, indent=4)
    redis.set(f'{file_name}_status', 'done')