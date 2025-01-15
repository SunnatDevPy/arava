from typing import Annotated, Optional

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel

from apps.models import User, Shop
from apps.models.users import MyAddress
from apps.routers import geolocator
from dispatcher import bot

user_router = APIRouter(prefix='/users', tags=['User'])


async def start(lang='uz'):
    if lang == 'uz':
        text = "Guruxga qo'shish"
    else:
        text = "Добавить в группу"
    kb = InlineKeyboardBuilder()
    kb.row(InlineKeyboardButton(text=text, url='https://t.me/stock_security_bot?startgroup=true'))
    kb.adjust(2)
    return kb.as_markup()


class UserAdd(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: Optional[str] = None
    contact: str
    is_active: Optional[bool] = False
    status: Optional[str] = "USER"
    type: Optional[str] = "ONE"
    long: Optional[float]
    lat: Optional[float]


class UserList(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    contact: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None
    type: Optional[str] = None
    long: Optional[float] = None
    lat: Optional[float] = None


class ShopsList(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    owner_id: Optional[int] = None
    shop_category_id: Optional[int] = None
    work_time: Optional[str] = None
    photos: Optional[str] = None
    group_id: Optional[int] = None
    long: Optional[float] = None
    lat: Optional[float] = None


@user_router.post("", name="Create User")
async def user_add(operator_id: int, user_create: Annotated[UserAdd, Form()]):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin"]:
            await User.create(**user_create.dict())
            return {'ok': True}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@user_router.get('', name="List User")
async def user_list() -> list[UserList]:
    users = await User.all()
    return users


@user_router.get('/my-shops', name="List User Shops")
async def user_list(user_id: int) -> list[ShopsList]:
    shops = await Shop.get_shops_from_user(user_id)
    return shops


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    contact: Optional[str] = None
    is_active: Optional[bool] = None
    long: Optional[float] = None
    lat: Optional[float] = None


class UserUpdateStatus(BaseModel):
    status: Optional[str] = None
    type: Optional[str] = None


@user_router.get("/profile", name="Detail User")
async def user_detail(user_id: int):
    user = await User.get(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@user_router.patch("/profile", name="Update User")
async def user_patch_update(operator_id: int, items: Annotated[UserUpdate, Form()]):
    user = await User.get(operator_id)
    if user and operator_id:
        update_data = {k: v for k, v in items.dict().items() if v is not None}
        if items.long and items.lat:
            location = geolocator.reverse(f"{items.lat}, {items.long}")
            address = location.raw['address']
            name = f"{address['county']}, {address['neighbourhood']}, {address['road']}"
            check_address = await MyAddress.get_from_name(name)
            if check_address == None:
                await MyAddress.create(user_id=operator_id, lat=items.lat, long=items.long,
                                       address=f"{address['county']}, {address['neighbourhood']}, {address['road']}")
        if update_data:
            await User.update(user.id, **update_data)
            return {"ok": True, "data": update_data}
        else:
            return {"ok": False, "message": "Nothing to update"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@user_router.patch("/status", name="Update Status")
async def user_add(operator_id: int, user_id: int, items: Annotated[UserUpdateStatus, Form()]):
    operator = await User.get(operator_id)
    user = await User.get(user_id)
    if operator:
        if operator.status.value in ['moderator', "admin", "superuser"]:
            if operator.status.value == "moderator" and items.status:
                raise HTTPException(status_code=404, detail="Moderator status o'zgartirolmaydi faqatgina typle larni")
            if items.status == 'string' or items.status == '':
                items.status = None
            if items.type == 'string' or items.type == '':
                items.type = None
            update_data = {k: v for k, v in items.dict().items() if v is not None}

            await User.update(user.id, **update_data)
            if items.status:
                if user.status.value == 'admin':
                    bot.send_message(user_id, "Assalomu aleykum status admingaga o'zgartirildi")
                elif user.status.value == "moderator":
                    bot.send_message(user_id, "Assalomu aleykum status moderatorga o'zgartirildi")
            elif items.type:
                if user.type.value == 'restorator':
                    bot.send_message(user_id, "Assalomu aleykum status restoratorga o'zgartirildi")
                elif user.type.value == "optom":
                    bot.send_message(user_id, "Assalomu aleykum status optomchiga o'zgartirildi")
            return {"ok": True, "data": update_data}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@user_router.delete("/")
async def user_delete(operator_id: int, user_id: int):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin"]:
            await User.delete(user_id)
            return {"ok": True, 'id': user_id}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@user_router.get(path='/login', name="Login")
async def list_category_shop(username: str, password: int):
    user = await User.get_from_username_and_id(password, username)
    if user.status.value != "user":
        return {"user": user}
    else:
        raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
