from typing import Annotated, Optional

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel

from apps.models import User

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


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    contact: Optional[str] = None
    is_active: Optional[bool] = None
    long: Optional[float] = None
    lat: Optional[float] = None


class UserUpdateStatus(BaseModel):
    user_id: Optional[int]
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
async def user_patch_update(user_id: int, items: Annotated[UserUpdate, Form()]):
    user = await User.get(user_id)
    if user:
        update_data = {k: v for k, v in items.dict().items() if v is not None}
        if update_data:
            await User.update(user.id, **update_data)
            return {"ok": True, "data": update_data}
        else:
            return {"ok": False, "message": "Nothing to update"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@user_router.patch("/status", name="Update Status")
async def user_add(operator_id: int, items: Annotated[UserUpdateStatus, Form()]):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin"]:
            update_data = {k: v for k, v in items.dict().items() if v is not None}
            if update_data:
                await User.update(user.id, **update_data)
                return {"ok": True, "data": update_data}
            else:
                return {"ok": False, "message": "Nothing to update"}
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
