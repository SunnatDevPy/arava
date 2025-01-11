from typing import Optional

from fastapi import APIRouter, Form
from fastapi import Response
from pydantic import BaseModel
from starlette import status

from apps.models import User, ShopProductCategory, Shop

shop_category_router = APIRouter(prefix='/shop-categories', tags=['Shop Categories'])


class ListCategories(BaseModel):
    id: int
    name: str
    shop_id: int
    parent_id: Optional[int] = None
    icon_name: Optional[str] = None


@shop_category_router.get(path='', name="Categories")
async def list_category_shop() -> list[ListCategories]:
    categories = await ShopProductCategory.all()
    return categories


@shop_category_router.get(path='/from-shop', name="List from Shop")
async def list_category_shop(shop_id: int):
    shop = await Shop.get(shop_id)
    if shop:
        category = await ShopProductCategory.get_shop_categories(shop_id)
        return category
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_category_router.post(path='/', name="Create Category")
async def list_category_shop(seller_id: int,
                             shop_id: int = Form(),
                             name: str = Form(),
                             parent_id: int = Form(default=None),
                             icon_name: str = Form(default=None),
                             ):
    seller = await User.get(seller_id)
    shop = await Shop.get(shop_id)
    if seller and shop:
        if seller.id == shop.owner_id or seller.status.value in ['moderator', "admin", "superuser"]:
            if parent_id == 0:
                parent_id = None
            categ = await ShopProductCategory.create(name=name, shop_id=shop_id, parent_id=parent_id,
                                                     icon_name=icon_name)
            return {"ok": True, "id": categ.id}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


# # Update Category
@shop_category_router.patch(path='/', name="Update Category")
async def list_category_shop(operator_id: int,
                             category_id: int,
                             name: str = Form(default=None),
                             parent_id: int = Form(default=None),
                             icon_name: str = Form(default=None),
                             ):
    user = await User.get(operator_id)
    if user:
        update_data = {k: v for k, v in
                       {"name": name, "parent_id": parent_id, "icon_name": icon_name} if
                       v is not None}
        if user.status.value in ['moderator', "admin", "superuser"]:
            shop = await ShopProductCategory.get(category_id)
            if shop:
                await ShopProductCategory.update(category_id, **update_data)
                return {"ok": True}
            else:
                return Response("Bunday sho'p id yo'q", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_category_router.delete(path='/', name="Delete Category")
async def list_category_shop(category_id: int, operator_id: int):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            category = await ShopProductCategory.get(category_id)
            if category:
                await ShopProductCategory.delete(category_id)
                return {"ok": True}
            else:
                return Response("Bunday sho'p id yo'q", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
