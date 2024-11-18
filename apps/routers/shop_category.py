from fastapi import APIRouter
from fastapi import Response
from pydantic import BaseModel
from starlette import status

from apps.models import ShopCategory

shop_category_router = APIRouter(prefix='/shop-category', tags=['Shop-Category'])


class CreateCategory(BaseModel):
    name: str


class GetCategory(BaseModel):
    id: int


class UpdateCategory(BaseModel):
    id: int
    name: str


# List Shop categoriya va Shoplar
@shop_category_router.get(path='/', name="All shop category")
async def list_category_shop():
    shop_category = await ShopCategory.all()
    return {'shop_category': shop_category}


# Get Shop categoriya TODO
@shop_category_router.get(path='/products', name="Get Shop Category and from Products")
async def list_category_shop(item: GetCategory):
    category = await ShopCategory.get(item.id)
    if category:
        shops = category.shop
        return {'shop-category': category, "shops": shops}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_category_router.get(path='/shop-category', name="Get Shop Category")
async def list_category_shop(item: GetCategory):
    category = await ShopCategory.get(item.id)
    if category:
        return {'shop-category': category}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_category_router.post(path='/shop-category', name="Create Shop Category")
async def list_category_shop(item: CreateCategory):
    try:
        category = await ShopCategory.create(name=item.name)
        return {'shop-category': await category}
    except:
        return Response("Yaratishda xatolik", status.HTTP_404_NOT_FOUND)


# Update Shop categoriya
@shop_category_router.patch(path='/shop-category', name="Update Shop Category")
async def list_category_shop(item: UpdateCategory):
    category = await ShopCategory.get(item.id)
    if category:
        await ShopCategory.update(category.id, name=item.name)
        return {'shop-category': category}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_category_router.delete(path='/shop-category', name="Delete Shop Category")
async def list_category_shop(category_id: int):
    try:
        await ShopCategory.delete(category_id)
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
    except:
        return Response("O'chirishda xatolik", status.HTTP_404_NOT_FOUND)
