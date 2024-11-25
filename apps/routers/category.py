import os

from fastapi import APIRouter, File, UploadFile, Form
from fastapi import Response
from starlette import status
from starlette.responses import FileResponse

from apps.models import ShopCategory, User, Category, Shop

category_router = APIRouter(prefix='/category', tags=['Categories'])


@category_router.get(path='', name="Categories")
async def list_category_shop():
    categories = await Category.all()
    return {"categories": categories}


@category_router.get(path='', name="Categories from Shop")
async def list_category_shop(seller_id: int, shop_id: int):
    seller = await User.get(seller_id)
    shop = await Shop.get(shop_id)
    if seller and shop:
        if shop.owner_id == seller_id or seller.status.value in ['moderator', "admin"]:
            return {'shop': shop}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


# @category_router.get(path='/products', name="Get Products From Category")
# async def list_category_shop(shop_id: int):
#     category = await Shop.get(shop_id)
#     if category:
#         products = category.products
#         return {'shop-category': category, "products": products}
#     else:
#         return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@category_router.post(path='/', name="Create Category")
async def list_category_shop(seller_id: int,
                             shop_id: int = Form(),
                             name: str = Form(),
                             parent_id: int = Form(default=None),
                             photo: UploadFile = File(),
                             ):
    seller = await User.get(seller_id)
    shop = await Shop.get(shop_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if seller and shop:
        if seller.id == shop.owner_id or seller.status.value in ['moderator', "admin"]:
            if parent_id:
                parent_id = parent_id
            else:
                parent_id = None
            await Category.create(name=name, shop_id=shop_id, parent_id=parent_id, photos=photo)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


# # Update Category
@category_router.patch(path='/', name="Update Category")
async def list_category_shop(operator_id: int,
                             category_id: int,
                             name: str = Form(default=None),
                             parent_id: int = Form(default=None),
                             photo: UploadFile = File(default=None),
                             ):
    user = await User.get(operator_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user:
        update_data = {k: v for k, v in
                       {"name": name, "parent_id": parent_id, "photo": photo} if
                       v is not None}
        if user.status.value in ['moderator', "admin"]:
            shop = await Category.get(category_id)
            if shop:
                await Category.update(category_id, **update_data)
                return {"ok": True}
            else:
                return Response("Bunday sho'p id yo'q", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@category_router.delete(path='/', name="Delete Category")
async def list_category_shop(category_id: int, operator_id: int):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin"]:
            category = await Category.get(category_id)
            if category:
                await Category.delete(category_id)
                return {"ok": True}
            else:
                return Response("Bunday sho'p id yo'q", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
