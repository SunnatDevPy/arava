from typing import Annotated, Optional

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import APIRouter, HTTPException, Form
from geopy import Nominatim
from pydantic import BaseModel

from apps.models import BotUser, Shop, AdminPanelUser
from apps.models.users import MyAddress
from dispatcher import bot

bot_user_router = APIRouter(prefix='/bot-users', tags=['Bot User'])

geolocator = Nominatim(user_agent="Backend")


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
    first_name: str
    last_name: str
    tg_username: Optional[str] = None
    contact: str
    is_active: Optional[bool] = False
    type: Optional[str] = "ONE"
    long: Optional[float]
    lat: Optional[float]


class UserList(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tg_username: Optional[str] = None
    contact: Optional[str] = None
    is_active: Optional[bool] = None
    type: Optional[str] = None
    long: Optional[float] = None
    lat: Optional[float] = None


@bot_user_router.post("", name="Create Bot User")
async def user_add(operator_id: int, user_create: Annotated[UserAdd, Form()]):
    user = await AdminPanelUser.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            result = await BotUser.create(**user_create.dict())
            return {'ok': True, "user": result}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@bot_user_router.get('', name="List Bot User")
async def user_list() -> list[UserList]:
    users = await BotUser.all()
    return users


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    tg_username: Optional[str] = None
    contact: Optional[str] = None
    is_active: Optional[bool] = None
    long: Optional[float] = None
    lat: Optional[float] = None


type: Optional[str] = None


@bot_user_router.get("/profile", name="Detail Bot User")
async def user_detail(user_id: int):
    user = await BotUser.get(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@bot_user_router.patch("/profile", name="Update Bot User")
async def user_patch_update(operator_id: int, items: Annotated[UserUpdate, Form()]):
    user = await BotUser.get(operator_id)
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
            await BotUser.update(user.id, **update_data)
            return {"ok": True, "data": update_data}
        else:
            return {"ok": False, "message": "Nothing to update"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@bot_user_router.patch("/type", name="Update Status")
async def user_add(operator_id: int, user_id: int, type=Form()):
    operator = await BotUser.get(operator_id)
    user = await BotUser.get(user_id)
    if operator:
        if operator.status.value in ['moderator', "admin", "superuser"]:

            await BotUser.update(user.id, type=type)
            if type:
                if user.type.value == 'restorator':
                    await bot.send_message(user_id, "Assalomu aleykum status restoratorga o'zgartirildi")
                elif user.type.value == "optom":
                    await bot.send_message(user_id, "Assalomu aleykum status optomchiga o'zgartirildi")
            return {"ok": True, "data": user}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@bot_user_router.delete("/")
async def user_delete(operator_id: int, user_id: int):
    user = await BotUser.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            await BotUser.delete(user_id)
            return {"ok": True, 'id': user_id}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")
