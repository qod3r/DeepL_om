from gzip import GzipFile
from io import BytesIO
from fastapi import File, UploadFile
import nibabel as nib

async def get_data_from_nii_file(file: bytes):
    compressed_stream = BytesIO(file)
    with GzipFile(
        fileobj=compressed_stream, mode='rb'
    ) as decompressed_stream:
        nifti_data = BytesIO(decompressed_stream.read())
    compressed_stream.close()
    nifti_image = nib.nifti1.Nifti1Image.from_bytes(nifti_data.read())
    data = nifti_image.get_fdata()
    
    return data