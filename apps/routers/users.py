from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Form
from pydantic import BaseModel

from apps.models import User

user_router = APIRouter(prefix='/users', tags=['User'])


class UserAdd(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: Optional[str] = None
    contact: str
    is_active: Optional[bool] = False
    status: Optional[str] = "USER"
    long: Optional[float]
    lat: Optional[float]


# class UserList(BaseModel):
#     id: Optional[int] = None
#     first_name: str
#     last_name: str
#     username: Optional[str] = None
#     contact: str
#     is_active: Optional[bool] = False
#     status: Optional[str] = "USER"
#     long: Optional[float]
#     lat: Optional[float]

@user_router.post("", name="Create User")
async def user_add(operator_id: int, user_create: Annotated[UserAdd, Depends()]):
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
async def user_list():
    users = await User.all()
    return users


@user_router.get("/profile", name="Detail User")
async def user_detail(user_id: int):
    user = await User.get(user_id)
    if user:
        return {"user": user}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@user_router.patch("/profile", name="Update User")
async def user_patch_update(user_id: Optional[int],
                            first_name: Optional[str] = Form(None),
                            last_name: Optional[str] = Form(None),
                            contact: Optional[str] = Form(None),
                            is_active: Optional[bool] = Form(None),
                            long: Optional[float] = Form(None),
                            lat: Optional[float] = Form(None)):
    user = await User.get(user_id)
    if user:
        update_data = {k: v for k, v in {"first_name": first_name,
                                         "last_name": last_name,
                                         "contact": contact,
                                         "is_active": is_active,
                                         "long": long,
                                         "lat": lat}.items() if v is not None}
        if update_data:
            await User.update(user.id, **update_data)
            return {"ok": True, "data": update_data}
        else:
            return {"ok": False, "message": "Nothing to update"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


# @user_router.patch("/profile", name="Update User")
# async def user_patch_update(
#         user_id: int = Form(),
#         first_name: Optional[str] = Form(None),
#         last_name: Optional[str] = Form(None),
#         contact: Optional[str] = Form(None),
#         is_active: Optional[bool] = Form(None),
#         long: Optional[float] = Form(None),
#         lat: Optional[float] = Form(None),
# ):
#     def clean_empty_strings(value):
#         return value if value != "" else None
#
#     update_data = {
#         "first_name": clean_empty_strings(first_name),
#         "last_name": clean_empty_strings(last_name),
#         "contact": clean_empty_strings(contact),
#         "is_active": is_active,
#         "long": long,
#         "lat": lat,
#     }
#     update_data = {k: v for k, v in update_data.items() if v is not None}
#     if update_data:
#         await User.update(user_id, **update_data)
#         return {"ok": True, "data": update_data}
#     else:
#         return {"ok": False, "message": "Nothing to update"}


@user_router.patch("/status", name="Update Status")
async def user_add(operator_id: int, user_id: int = Form(), status: str = Form()):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin"]:
            try:
                await User.update(user_id, status=status)
                return {'ok': True}
            except:
                raise HTTPException(status_code=404, detail="Status kiritishda xatolik")
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
