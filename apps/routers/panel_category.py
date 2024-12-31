from typing import Optional

from fastapi import APIRouter, Form
from fastapi import Response
from pydantic import BaseModel
from starlette import status

from apps.models import User, Shop
from apps.models.products_model import PanelCategory

panel_category_router = APIRouter(prefix='/panel-category', tags=['Admin Panel Categories'])


class ListCategories(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None
    icon_name: Optional[str] = None


@panel_category_router.get(path='', name="Panel Categories")
async def list_category_shop() -> list[ListCategories]:
    categories = await PanelCategory.all()
    return categories


@panel_category_router.post(path='/', name="Create Panel Category")
async def list_category_shop(moderator_id: int,
                             name: str = Form(),
                             parent_id: int = Form(default=None),
                             icon_name: str = Form(default=None),
                             ):
    seller = await User.get(moderator_id)
    if seller:
        if seller.status.value in ['moderator', "admin", "superuser"]:
            if parent_id == 0:
                parent_id = None
            await PanelCategory.create(name=name, parent_id=parent_id, icon_name=icon_name)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


# # Update Category
@panel_category_router.patch(path='/', name="Update Panel Category")
async def list_category_shop(moderator_id: int,
                             category_id: int,
                             name: str = Form(default=None),
                             parent_id: int = Form(default=None),
                             icon_name: str = Form(default=None),
                             ):
    user = await User.get(moderator_id)
    if user:
        update_data = {k: v for k, v in
                       {"name": name, "parent_id": parent_id, "icon_name": icon_name} if
                       v is not None}
        if user.status.value in ['moderator', "admin", "superuser"]:
            shop = await PanelCategory.get(category_id)
            if shop:
                await PanelCategory.update(category_id, **update_data)
                return {"ok": True}
            else:
                return Response("Bunday sho'p id yo'q", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@panel_category_router.delete(path='/', name="Delete Category")
async def list_category_shop(category_id: int, operator_id: int):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            category = await PanelCategory.get(category_id)
            if category:
                await PanelCategory.delete(category_id)
                return {"ok": True}
            else:
                return Response("Bunday sho'p id yo'q", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
