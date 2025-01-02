from typing import Annotated, Optional

from fastapi import APIRouter
from fastapi import Response
from fastapi.params import Form
from pydantic import BaseModel
from starlette import status

from apps.models import ShopCategory, User, Shop

category_router = APIRouter(prefix='/main-category', tags=['Main Shop Category'])


class CreateShopCategory(BaseModel):
    name: str
    icon_name: str


class ListShopCategory(BaseModel):
    id: int
    name: str
    icon_name: str


class UpdateShopCategory(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    icon_name: Optional[str] = None


# List Shop categoriya va Shoplar
@category_router.get(path='', name="All shop category")
async def list_category_shop():
    shop_category = await ShopCategory.all()
    return shop_category


@category_router.get(path='/detail', name="Get Shop Category Detail")
async def list_category_shop(shop_category_id: int):
    category = await ShopCategory.get(shop_category_id)
    if category:
        return {'shop-category': category}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@category_router.get(path='/shops', name="Get Shops in Shop-Category")
async def list_category_shop(shop_category_id: int):
    category = await ShopCategory.get(shop_category_id)
    if category:
        shops = await Shop.get_shops_category(shop_category_id)
        return {'shops': shops}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@category_router.post(path='', name="Create Shop Category")
async def list_category_shop(operator_id: int, items: Annotated[CreateShopCategory, Form()]):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            await ShopCategory.create(name=items.name, icon_name=items.icon_name)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


# Update Shop categoriya
@category_router.patch(path='', name="Update Shop Category")
async def list_category_shop(operator_id: int, items: Annotated[UpdateShopCategory, Form()]):
    shop_category = await ShopCategory.get(items.shop_category_id)
    user = await User.get(operator_id)
    if user and shop_category:
        if user.status.value in ['moderator', "admin", "superuser"]:
            name = None
            icon_name = None
            if items.name:
                pass
            if shop_category:
                await ShopCategory.update(items.shop_category_id, name=items.shop_category_id)
                return {"ok": True}
        else:
            return Response("Userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@category_router.delete(path='/shop-category', name="Delete Shop Category")
async def list_category_shop(operator_id: int, category_id: int):
    user = await User.get(operator_id)
    category = await ShopCategory.get(category_id)
    if user and category:
        if user.status.value in ['moderator', "admin", "superuser"]:
            await ShopCategory.delete(category_id)
            return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)