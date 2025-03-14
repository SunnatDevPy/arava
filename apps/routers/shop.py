from typing import Optional, Annotated

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi import Response
from pydantic import BaseModel
from starlette import status

from apps.models import AdminPanelUser, Shop, ShopPhoto, WorkTimes, ShopCategory, BotUser

shop_router = APIRouter(prefix='/shop', tags=['Shop'])


class ListShopsModel(BaseModel):
    id: Optional[int]
    owner_id: Optional[int]
    name: Optional[str]
    work_status: Optional[str]
    lat: Optional[float]
    long: Optional[float]
    shop_category_id: Optional[int]
    group_id: Optional[int] = None
    photo: Optional[str] = None
    rating: Optional[int] = None


class UpdateShopsModel(BaseModel):
    owner_id: Optional[int] = None
    name: Optional[str] = None
    work_status: Optional[str] = None
    lat: Optional[float] = None
    long: Optional[float] = None
    group_id: Optional[int] = None
    shop_category_id: Optional[int] = None
    photo: Optional[str] = None
    rating: Optional[int] = None


@shop_router.get(path='', name="Shops")
async def list_category_shop():
    shops = await Shop.all()
    return {"shops": shops, "work": await WorkTimes.all()}


@shop_router.get(path='/search', name="search")
async def list_category_shop(search: Optional[str] = None, main_category_id: Optional[int] = None):
    category = await ShopCategory.get(main_category_id)
    if category:
        shops = await Shop.search_shops(search, main_category_id)
    else:
        shops = await Shop.search_shops(search)
    return {"shops": shops}


@shop_router.get(path='/detail', name="Get Shop")
async def list_category_shop(shop_id: int):
    shop = await Shop.get(shop_id)
    if shop:
        return {'shop': shop}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_router.get(path='/from-user', name="Get Shop from User")
async def list_category_shop(user_id: int):
    shop = await Shop.get_shops_from_user(user_id)
    if shop:
        return {'shops': shop}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_router.get(path='/from-category', name="Get Shops in Shop-Category")
async def list_category_shop(shop_category_id: int):
    shops = await Shop.get_shops_category(shop_category_id)
    return shops


@shop_router.post(path='', name="Create Shop")
async def list_category_shop(operator_id: int,
                             owner_id: int = Form(),
                             name: str = Form(),
                             lat: float = Form(),
                             long: float = Form(),
                             group_id: int = Form(default=None),
                             shop_category_id: int = Form(default=None),
                             discount_price: int = Form(default=None),
                             photo: UploadFile = File(default=None)):
    user = await AdminPanelUser.get(operator_id)
    seller = AdminPanelUser.get(owner_id) # Todo filter seller
    if user and seller:
        if user.status.value in ['moderator', "admin", "superuser"]:
            shop = await Shop.create(owner_id=owner_id, name=name, lat=lat, long=long, group_id=group_id,
                                     main_category_id=shop_category_id, photo=photo, work_status='CLOSE',
                                     rating=0, discount_price=discount_price)
            return {"ok": True, "shop_id": shop.id}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


# Update Shop
@shop_router.patch(path='', name="Update Shop")
async def list_category_shop(operator_id: int,
                             shop_id: int = Form(),
                             name: str = Form(default=None),
                             lat: float = Form(default=None),
                             long: float = Form(default=None),
                             group_id: int = Form(default=None),
                             shop_category_id: int = Form(default=None),
                             discount_price: int = Form(default=None),
                             photo: UploadFile = File(default=None)):
    user = await AdminPanelUser.get(operator_id)
    shop = await Shop.get(shop_id)
    if user and shop:
        if photo:
            if not photo.content_type.startswith("image/"):
                return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
        update_data = {k: v for k, v in {"shop_id": shop_id,
                                         "name": name,
                                         "lat": lat,
                                         "long": long,
                                         "group_id": group_id,
                                         "shop_category_id": shop_category_id,
                                         "discount_price": discount_price}.items() if v is not None}
        if user.status.value in ['moderator', "admin", "superuser"] or user.id == shop.owner_id:
            await Shop.update(shop_id, **update_data)
            return {"ok": True, "shop": shop}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_router.delete(path='', name="Delete Shop")
async def list_category_shop(operator_id: int, shop_id: int):
    user = await AdminPanelUser.get(operator_id)
    shop = await Shop.get(shop_id)
    if user and shop:
        if user.status.value in ["moderator", "admin", "superuser"]:
            await Shop.delete(shop)
            return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
        else:
            return Response("AdminPanelUserda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


class ListPhotosShopModel(BaseModel):
    id: int
    shop_id: int
    photo: str


@shop_router.get(path='/photos', name="Get Shop Photos")
async def list_category_shop(shop_id: int) -> list[ListPhotosShopModel]:
    shop = await ShopPhoto.get_shop_photos(shop_id)
    if shop:
        return shop


@shop_router.post(path='/photos', name="Create Shop Photo")
async def list_category_shop(operator_id: int, shop_id: int, photo: UploadFile = File()):
    user = await AdminPanelUser.get(operator_id)
    shop = await Shop.get(shop_id)
    if photo:
        if not photo.content_type.startswith("image/"):
            return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user and shop:
        if user.status.value in ['moderator', "admin", "superuser"] or user.id == shop.owner_id:
            shop_photo = await ShopPhoto.create(shop_id=shop_id, photo=photo)
            return {"ok": True, "id": shop_photo.id}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_router.patch(path='/photos', name="Update Shop Photo")
async def list_category_shop(operator_id: int, shop_photo_id: int, photo: UploadFile = File()):
    user = await AdminPanelUser.get(operator_id)
    shop_photo = await ShopPhoto.get(shop_photo_id)
    if photo:
        if not photo.content_type.startswith("image/"):
            return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user and shop_photo:
        if user.status.value in ['moderator', "admin", "superuser"]:
            await ShopPhoto.update(shop_photo.id, photo=photo)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@shop_router.delete("/photos")
async def user_delete(operator_id: int, shop_photo_id):
    user = await AdminPanelUser.get(operator_id)
    shop_photo = await ShopPhoto.get(shop_photo_id)
    if user and shop_photo:
        if user.status.value in ['moderator', "admin", "superuser"]:
            await ShopPhoto.delete(shop_photo_id)
            return {"ok": True, 'id': shop_photo_id}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")
