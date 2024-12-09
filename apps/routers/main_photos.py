import os
import uuid

from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi import Response
from starlette import status
from starlette.responses import FileResponse

from apps.models import MainPhoto, User
from apps.routers.minio_storage import minioClient

main_photos_router = APIRouter(prefix='/banners', tags=['Banners'])

minio_url = "http://127.0.0.1:9001/browser/"


@main_photos_router.get(path='', name="All banner photos")
async def list_category_shop():
    photos = await MainPhoto.all()
    return {'photos': photos}


@main_photos_router.post(path='', name="Create Banner Photo")
async def list_category_shop(operator_id: int, photo: UploadFile = File()):
    user = await User.get(operator_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            file_extension = photo.filename.split(".")[-1]
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            try:
                minioClient.put_object(
                    "arava",
                    unique_filename,
                    photo.file,
                    length=-1,  # Для стриминга неизвестного размера
                    part_size=10 * 1024 * 1024,
                    content_type=photo.content_type
                )
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")
            image_url = f"{minio_url}/arava/{unique_filename}"
            await MainPhoto.create(photo=image_url)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("User yo'q", status.HTTP_404_NOT_FOUND)


@main_photos_router.patch(path='/update', name="Update Banner photo")
async def list_category_shop(operator_id: int, photo: UploadFile = File(), photo_id: int = Form()):
    user = await User.get(operator_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            if await MainPhoto.get(photo_id):
                await MainPhoto.update(photo_id, photos=photo)
                return {"ok": True}
            else:
                return Response("Bunday idli rasim yo'q", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("User yo'q", status.HTTP_404_NOT_FOUND)


@main_photos_router.delete(path='/', name="Delete Banner photo")
async def list_category_shop(operator_id: int, photo_id: int = Form()):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            if await MainPhoto.get(photo_id):
                await MainPhoto.delete(photo_id)
                return {"ok": True}
            else:
                return Response("Bunday idli rasim yo'q", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("User yo'q", status.HTTP_404_NOT_FOUND)
