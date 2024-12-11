from fastapi import APIRouter
from fastapi import Response
from starlette import status

from apps.models import User, Shop, Cart, Order, OrderItem
from apps.utils.details import sum_from_shop

order_router = APIRouter(prefix='/order', tags=['Orders'])


@order_router.get(path='', name="Orders")
async def list_category_shop():
    orders = await Order.all()
    return {"orders": orders}


@order_router.get(path='/detail', name="Get Cart")
async def list_category_shop(cart_id: int):
    cart = await Order.get(cart_id)
    if cart:
        return {'order': cart}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@order_router.get(path='/from-user', name="Get Cart from User")
async def list_category_shop(user_id: int):
    orders = await Order.get_cart_from_user(user_id)
    if orders:
        return {'orders': orders}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@order_router.get(path='/from-user-shop', name="Get Cart from User in Shop")
async def list_category_shop(user_id: int, shop_id: int):
    orders = await Order.get_cart_from_shop(user_id, shop_id)
    if orders:
        return {'orders': orders}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@order_router.post(path='', name="Create Order from User")
async def list_category_shop(client_id: int,
                             shop_id: int):
    user = await User.get(client_id)
    shop = await Shop.get(shop_id)
    if user and shop:
        carts: list['Cart'] = await Cart.get_cart_from_shop(client_id, shop_id)
        sum = await sum_from_shop(shop_id, user)
        order = await Order.create(user_id=client_id, payment=False, status="NEW", shop_id=shop_id, total_sum=sum)
        for i in carts:
            await OrderItem.create(product_id=i.product_id, order_id=order.id, count=i.count)
            await Cart.delete(i.id)
        return {"ok": True, "message": "Buyurtma qabul qilindi va guruxga yuborildi ", "drive_price": 5000, "time": 60}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)

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
