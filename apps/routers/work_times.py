from typing import Optional, Annotated

from fastapi import APIRouter, Form, HTTPException
from fastapi import Response
from pydantic import BaseModel
from starlette import status

from apps.models import User, Shop, Cart, WorkTimes
from apps.utils.details import sum_from_shop, get_shops_unique_cart, detail_cart, get_carts_

work_router = APIRouter(prefix='/work', tags=['Work Shop'])


@work_router.get(path='', name="Work all")
async def list_category_shop():
    works = await WorkTimes.all()
    return {"works": works}


@work_router.get(path='/detail', name="Get Work")
async def list_category_shop(work_id: int):
    work = await WorkTimes.get(work_id)
    if work:
        return work
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@work_router.get(path='/from_shop', name="Get Work in Shop")
async def list_category_shop(shop_id: int):
    return {"works": await WorkTimes.from_shop(shop_id)}


@work_router.post(path='', name="Create Work from User")
async def list_category_shop(client_id: int,
                             shop_id: int = Form(),
                             open_time: str = Form(),
                             close_time: str = Form(),
                             weeks: list = Form()):
    user = await User.get(client_id)
    shop = await Shop.get(shop_id)
    if user and shop:
        await WorkTimes.create(shop_id=shop_id, open_time=open_time, close_time=close_time, weeks=weeks)
        return {"ok": True}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


class UpdateWork(BaseModel):
    open_time: Optional[str] = None
    close_time: Optional[str] = None
    weeks: Optional[list] = None


@work_router.patch(path='', name="Update Work")
async def list_category_shop(user_id: int, shop_id: int, work_id: int, items: Annotated[UpdateWork, Form()]):
    work = await WorkTimes.get(work_id)
    user = await User.get(user_id)
    shop = await Shop.get(shop_id)
    if user.status.value in ["moderator", "admin", "superuser"] or user_id == shop.owner_id:
        if work:
            update_data = {k: v for k, v in items.dict().items() if v is not None}
            await WorkTimes.update(work_id, **update_data)
            return {"ok": True}
        else:
            return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Bu userda xuquq yoq", status.HTTP_404_NOT_FOUND)
