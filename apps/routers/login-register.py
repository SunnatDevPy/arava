from typing import Annotated, Optional

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from fastapi import APIRouter, HTTPException, Form
from pydantic import BaseModel

from apps.models import AdminPanelUser, Shop

login_register_router = APIRouter(tags=['Login'])


class UserAdd(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: Optional[str] = None
    password: Optional[str] = None
    contact: Optional[str] = None
    is_active: Optional[bool] = False
    status: Optional[str] = "seller"


class UserLogin(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None


@login_register_router.get(path='/login', name="Login")
async def list_category_shop(items: Annotated[UserLogin, Form()]):
    user = await AdminPanelUser.get_from_username_and_password(items.password, items.username)
    if user:
        return {"user": user}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@login_register_router.get(path='/register', name="Register")
async def list_category_shop(items: Annotated[UserAdd, Form()]):
    try:
        user = await AdminPanelUser.create(**items.dict())
        return {"user": user}
    except:
        raise HTTPException(status_code=404, detail="Item not found")
