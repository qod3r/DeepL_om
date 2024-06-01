from fastapi import APIRouter, File, UploadFile

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
    #TODO: check that file is valid
    # file_bytes = await file.read()
    # file_hash = sha256(file_bytes)
    # nii_data = await get_data_from_nii_file(file)
    # paths = fdata_to_temp_imgs(nii_data, Path('temp/'))
    # masks = await model.predict_tempdir_async(paths)

    # mask_new = []

    # for mask in masks:
    #     mask_new.append(json.dumps(mask.to_dict()).encode('utf-8'))

    
    
    # await StudiesDAO.add_one(study=study)
    pass


@router.get("/status/{hash}")
def get_status(hash: str):
    pass