from typing import Annotated, Optional

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel

from apps.models import AdminPanelUser, Shop

panel_user_router = APIRouter(prefix='/panel-users', tags=['Panel User'])


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
    password: Optional[str] = None
    contact: Optional[str] = None
    is_active: Optional[bool] = False
    status: Optional[str] = "seller"


class UserList(BaseModel):
    id: Optional[int] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None
    status: Optional[str] = None
    contact: Optional[str] = None


class ShopsList(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    owner_id: Optional[int] = None
    main_category_id: Optional[int] = None
    work_time: Optional[str] = None
    photos: Optional[str] = None
    group_id: Optional[int] = None
    long: Optional[float] = None
    lat: Optional[float] = None


@panel_user_router.post("", name="Create Panel User")
async def user_add(user_create: Annotated[UserAdd, Form()]):
    try:
        user = await AdminPanelUser.create(**user_create.dict())
        return {'ok': True, "user": user}
    except:
        raise HTTPException(status_code=404, detail="Item not found")


@panel_user_router.get('', name="List Panel User")
async def user_list() -> list[UserList]:
    users = await AdminPanelUser.all()
    return users


@panel_user_router.get('/my-shops', name="List User Shops")
async def user_list(seller_user_id: int) -> list[ShopsList]:
    shops = await Shop.get_shops_from_user(seller_user_id)
    return shops


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    contact: Optional[str] = None
    is_active: Optional[bool] = None


@panel_user_router.get("/profile", name="Detail Panel User")
async def user_detail(user_id: int):
    user = await AdminPanelUser.get(user_id)
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@panel_user_router.patch("/profile", name="Update User")
async def user_patch_update(user_id: int, items: Annotated[UserUpdate, Form()]):
    user = await AdminPanelUser.get(user_id)
    if user and user_id:
        update_data = {k: v for k, v in items.dict().items() if v is not None}
        if update_data:
            await AdminPanelUser.update(user.id, **update_data)
            return {"ok": True, "data": update_data}
        else:
            return {"ok": False, "message": "Nothing to update"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@panel_user_router.patch("/status", name="Update Status")
async def user_add(operator_id: int, user_id: int, status: str = Form()):
    operator = await AdminPanelUser.get(operator_id)
    user = await AdminPanelUser.get(user_id)
    if operator:
        if operator.status.value in ["admin", "superuser"]:
            if status == 'string' or status == '':
                status = None
            await AdminPanelUser.update(user.id, status=status)
            return {"ok": True, "user": user}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@panel_user_router.delete("/")
async def user_delete(operator_id: int, user_id: int):
    user = await AdminPanelUser.get(operator_id)
    if user:
        if user.status.value in ["admin", "superuser"]:
            await AdminPanelUser.delete(user_id)
            return {"ok": True, 'id': user_id}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")


class UserLogin(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


@panel_user_router.get(path='/login', name="Login")
async def list_category_shop(items: Annotated[UserLogin, Form()]):
    user = await AdminPanelUser.get_from_username_and_password(items.password, items.username)
    if user:
        return {"user": user}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@panel_user_router.get(path='/register', name="Login")
async def list_category_shop(items: Annotated[UserAdd, Form()]):
    try:
        user = await AdminPanelUser.create(**items.dict())
        return {"user": user}
    except:
        raise HTTPException(status_code=404, detail="Item not found")
