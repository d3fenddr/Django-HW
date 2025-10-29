from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
import cloudinary
import cloudinary.uploader
import os
from ..deps import get_current_user


router = APIRouter()


@router.post('/image')
async def upload_image(file: UploadFile = File(...), user=Depends(get_current_user)):
    url = os.getenv('CLOUDINARY_URL')
    if not url:
        raise HTTPException(500, detail='Cloudinary not configured')
    # Ensure cloudinary is configured from env
    cloudinary.config(cloudinary_url=url)
    try:
        res = cloudinary.uploader.upload(file.file, folder='habr', resource_type='image')
        return {"url": res.get('secure_url') or res.get('url')}
    except Exception as e:
        raise HTTPException(400, detail=str(e))


