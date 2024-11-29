from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi import Response
from starlette import status

from apps.models import User, Shop, ShopPhoto, Cart

cart_router = APIRouter(prefix='/carts', tags=['Cart'])


@cart_router.get(path='', name="Carts")
async def list_category_shop():
    carts = await Cart.all()
    return {"carts": carts}


@cart_router.get(path='/detail', name="Get Cart")
async def list_category_shop(cart_id: int):
    cart = await Cart.get(cart_id)
    if cart:
        return {'cart': cart}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@cart_router.get(path='/from-user', name="Get Cart")
async def list_category_shop(user_id: int):
    carts = await Cart.from_user(user_id)
    if carts:
        return {'carts': carts}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)

#
# @shop_router.post(path='', name="Create Shop")
# async def list_category_shop(operator_id: int,
#                              owner_id: int = Form(...),
#                              name: str = Form(),
#                              long: float = Form(default=None),
#                              lat: float = Form(default=None),
#                              shop_category_id: int = Form(),
#                              photo: UploadFile = File(default=None),
#                              ):
#     user = await User.get(operator_id)
#     if not photo.content_type.startswith("image/"):
#         return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
#     if user:
#         if user.status.value in ['moderator', "admin"]:
#             await Shop.create(name=name, owner_id=owner_id, work_time='CLOSE', photos=photo,
#                               shop_category_id=shop_category_id, long=long, lat=lat)
#             return {"ok": True}
#         else:
#             return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
#     else:
#         return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
#
#
# # Update Shop
# @shop_router.patch(path='', name="Update Shop")
# async def list_category_shop(operator_id: int,
#                              shop_id: int = Form(),
#                              name: str = Form(default=None),
#                              long: float = Form(default=None),
#                              lat: float = Form(default=None),
#                              shop_category_id: int = Form(default=None),
#                              work_time: str = Form(default="CLOSE"),
#                              photo: UploadFile = File(default=None),
#                              ):
#     user = await User.get(operator_id)
#     shop = await Shop.get(shop_id)
#     if not photo.content_type.startswith("image/"):
#         return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
#     if user and shop:
#         update_data = {k: v for k, v in
#                        {"name": name, "shop_category_id": shop_category_id, "photo": photo,
#                         "work_time": work_time, "log": long, "lat": lat}.items() if
#                        v is not None}
#
#         if user.status.value in ['moderator', "admin"] or user.id == shop.owner_id:
#             await Shop.update(shop_id, **update_data)
#             return {"ok": True}
#         else:
#             return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
#     else:
#         return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
#
#
# @shop_router.delete(path='', name="Delete Shop")
# async def list_category_shop(operator_id: int, shop_id: int):
#     user = await User.get(operator_id)
#     shop = await Shop.get(shop_id)
#     if user and shop:
#         if user.status.value in ['moderator', "admin"]:
#             await Shop.delete(shop)
#             return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
#         else:
#             return Response("Userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
#     else:
#         return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
#
#
# @shop_router.get(path='/photos', name="Get Shop Photos")
# async def list_category_shop(shop_id: int):
#     shop = await Shop.get(shop_id)
#     if shop:
#         return {'shop_photos': await ShopPhoto.all()}
#     else:
#         return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
#
#
# @shop_router.post(path='/photos', name="Create Shop Photo")
# async def list_category_shop(operator_id: int,
#                              shop_id: int = Form(),
#                              photo: UploadFile = File(default=None),
#                              ):
#     user = await User.get(operator_id)
#     shop = await Shop.get(shop_id)
#     if not photo.content_type.startswith("image/"):
#         return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
#     if user and shop:
#         if user.status.value in ['moderator', "admin"] or user.id == shop.owner_id:
#             await ShopPhoto.create(shop_id=shop_id, photo=photo)
#             return {"ok": True}
#         else:
#             return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
#     else:
#         return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
#
#
# @shop_router.patch(path='/photos', name="Update Shop Photo")
# async def list_category_shop(operator_id: int,
#                              shop_id: int = Form(),
#                              shop_photo_id: int = Form(),
#                              photo: UploadFile = File(default=None),
#                              ):
#     user = await User.get(operator_id)
#     shop = await ShopPhoto.get(shop_id)
#     if not photo.content_type.startswith("image/"):
#         return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
#     if user and shop:
#         update_data = {k: v for k, v in
#                        {"photo": photo}.items() if
#                        v is not None}
#         if user.status.value in ['moderator', "admin"] or user.id == shop.owner_id:
#             await ShopPhoto.update(shop_photo_id, **update_data)
#             return {"ok": True}
#         else:
#             return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
#     else:
#         return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
#
#
# @shop_router.delete("/photos")
# async def user_delete(operator_id: int, shop_photo_id):
#     user = await User.get(operator_id)
#     if user:
#         if user.status.value in ['moderator', "admin"]:
#             await ShopPhoto.delete(shop_photo_id)
#             return {"ok": True, 'id': shop_photo_id}
#         else:
#             raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
#     else:
#         raise HTTPException(status_code=404, detail="Item not found")
