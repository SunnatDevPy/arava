from typing import List

from fastapi import APIRouter, UploadFile, File, Form
from fastapi import Response
from starlette import status
import os
from apps.models import MainPhoto, AdminPanelUser

main_photos_router = APIRouter(prefix='/banners', tags=['Banners'])


@main_photos_router.get(path='', name="All banner photos")
async def list_category_shop():
    photos = await MainPhoto.all()
    return {'photos': photos}

# @main_photos_router.get(path='', name="All banner photos")
# async def get_photos() -> List[str]:
#     # Возвращаем список всех фотографий в папке
#     return [file for file in os.listdir("media/banner") if os.path.isfile(os.path.join("media/banner", file))]


@main_photos_router.post(path='', name="Create Banner Photo")
async def list_category_shop(operator_id: int, photo: UploadFile = File()):
    user = await AdminPanelUser.get(operator_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            await MainPhoto.create(photo=photo)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("User yo'q", status.HTTP_404_NOT_FOUND)


@main_photos_router.patch(path='/update', name="Update Banner photo")
async def list_category_shop(operator_id: int, photo: UploadFile = File(), photo_id: int = Form()):
    user = await AdminPanelUser.get(operator_id)
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
    user = await AdminPanelUser.get(operator_id)
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
