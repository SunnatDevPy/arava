from typing import Annotated

from fastapi import APIRouter
from fastapi import Response
from fastapi.params import Form
from pydantic import BaseModel
from starlette import status

from apps.models import ShopCategory, User

shop_category_router = APIRouter(prefix='/shop-category', tags=['Shop-Category'])


class CreateShopCategory(BaseModel):
    name: str


class ListShopCategory(BaseModel):
    id: int
    name: str


class UpdateShopCategory(BaseModel):
    shop_category_id: int
    name: str


# List Shop categoriya va Shoplar
@shop_category_router.get(path='', name="All shop category")
async def list_category_shop():
    shop_category = await ShopCategory.all()
    return shop_category


@shop_category_router.get(path='/detail', name="Get Shop Category Detail")
async def list_category_shop(shop_category_id: int):
    category = await ShopCategory.get(shop_category_id)
    if category:
        return {'shop-category': category}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_category_router.post(path='/shop-category', name="Create Shop Category")
async def list_category_shop(operator_id: int, items: Annotated[CreateShopCategory, Form()]):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            await ShopCategory.create(name=items.name)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


# Update Shop categoriya
@shop_category_router.patch(path='/shop-category', name="Update Shop Category")
async def list_category_shop(operator_id: int, items: Annotated[UpdateShopCategory, Form()]):
    shop_category = await ShopCategory.get(items.shop_category_id)
    user = await User.get(operator_id)
    if user and shop_category:
        if user.status.value in ['moderator', "admin"]:
            if shop_category:
                await ShopCategory.update(items.shop_category_id, name=items.shop_category_id)
                return {"ok": True}
        else:
            return Response("Userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_category_router.delete(path='/shop-category', name="Delete Shop Category")
async def list_category_shop(operator_id: int, category_id: int):
    user = await User.get(operator_id)
    category = await ShopCategory.get(category_id)
    if user and category:
        if user.status.value in ['moderator', "admin"]:
            await ShopCategory.delete(category_id)
            return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
