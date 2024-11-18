import os

from fastapi import APIRouter, File, UploadFile, Form
from fastapi import Response
from starlette import status
from starlette.responses import FileResponse

from apps.models import ShopCategory, User, Shop

shop_router = APIRouter(prefix='/shop', tags=['Shop'])


@shop_router.get("/photos", name="Banner photos")
async def list_photo_banner():
    list_ = []
    image_path = os.listdir('media/shop')
    if not image_path:
        return Response("Image not found on the server", status.HTTP_404_NOT_FOUND)
    for i in image_path:
        file_path = 'media/shop/' + i
        if i.endswith('png'):
            type = 'png'
        else:
            type = 'jpeg'
        list_.append(FileResponse(file_path, media_type=f"image/{type}", filename=i))
    return {"banner": list_}


# List Shop categoriya va Shoplar
@shop_router.get(path='', name="Shops")
async def list_category_shop():
    shops = await Shop.all()
    return {"shops": shops}


# Get Shop categoriya TODO
@shop_router.get(path='/detail', name="Get Shop")
async def list_category_shop(shop_id: int):
    category = await Shop.get(shop_id)
    if category:
        products = category.products
        return {'shop-category': category, "products": products}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_router.post(path='/', name="Create Shop")
async def list_category_shop(operator_id: int,
                             name: str = Form(...),
                             owner_id: int = Form(...),
                             shop_category_id: int = Form(...),
                             photo: UploadFile = File(...),
                             ):
    user = await User.get(operator_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user:
        if user.status.value in ['moderator', "admin"]:
            await Shop.create(name=name, owner_id=owner_id, work_time='CLOSE', photos=photo,
                              shop_category_id=shop_category_id)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


# Update Shop
@shop_router.patch(path='/', name="Update Shop")
async def list_category_shop(operator_id: int,
                             shop_id: int = Form(),
                             name: str | None = Form(default=None),
                             owner_id: int | None = Form(...),
                             shop_category_id: int | None = Form(),
                             work_time: str | None = Form(default="CLOSE"),
                             photo: UploadFile | None = File(),
                             ):
    user = await User.get(operator_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user:
        update_data = {k: v for k, v in
                       {"name": name, "owner_id": owner_id, "shop_category_id": shop_category_id, "photo": photo} if
                       v is not None}
        if user.status.value in ['moderator', "admin"]:
            shop = await Shop.get(shop_id)
            if shop:
                await Shop.update(shop_id, **update_data)
                return {"ok": True}
            else:
                return Response("Bunday sho'p id yo'q", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_router.delete(path='/shop-category', name="Delete Shop Category")
async def list_category_shop(category_id: int):
    try:
        await ShopCategory.delete(category_id)
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
    except:
        return Response("O'chirishda xatolik", status.HTTP_404_NOT_FOUND)


'''
========================================================
Bozorlar bilan ishlash
'''


@shop_router.get(path='/', name="Shops")
async def list_():
    shop_category = await ShopCategory.all()
    shops = await Shop.all()
    return {'shop_category': shop_category, "shops": Shop}
