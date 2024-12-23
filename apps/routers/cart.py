from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi import Response
from starlette import status

from apps.models import User, Shop, ShopPhoto, Cart, Product
from apps.utils.details import sum_from_shop, get_shops_unique_cart, detail_cart, get_carts_

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


@cart_router.get(path='/sum', name="Get Cart Sum User")
async def list_category_shop(user_id: int, shop_id: int):
    user = await User.get(user_id)
    shop = await Shop.get(shop_id)
    if shop and user:
        sum_ = await sum_from_shop(shop_id, user)
        return sum_[0]
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@cart_router.get(path='/from-user', name="Get Cart")
async def list_category_shop(user_id: int):
    carts = await Cart.get_cart_from_user(user_id)
    return {'carts': carts}


@cart_router.get(path='/from-user-shop', name="Get Cart in Shop")
async def list_category_shop(user_id: int, shop_id: int):
    carts = await detail_cart(shop_id, user_id)
    return {'carts': carts, "shops": await get_shops_unique_cart(carts)}


@cart_router.get(path='/shop_by_user', name="Get Cart in Shop")
async def list_category_shop(user_id: int):
    return {"shops": await get_carts_(user_id)}


@cart_router.post(path='', name="Create Cart from User")
async def list_category_shop(client_id: int,
                             product_id: int = Form(),
                             shop_id: int = Form(),
                             count: int = Form()):
    user = await User.get(client_id)
    cart = await Cart.get_cart_from_product(client_id, product_id)
    if user and product_id:
        if cart:
            await Cart.update(cart.id, count=count + cart.count)
        else:
            await Cart.create(user_id=user.id, product_id=product_id, count=count, shop_id=shop_id)
        return {"ok": True}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@cart_router.delete("/delete-product", name="Delete Product in cart")
async def user_delete(user_id: int, product_id: int):
    cart = await Cart.get_cart_from_product(user_id, product_id)
    if cart:
        await Cart.delete(cart.id)
        return {"ok": True}
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@cart_router.patch(path='', name="Update Cart")
async def list_category_shop(user_id: int, cart_id: int, count: int):
    cart = await Cart.get(cart_id)
    if cart:
        await Cart.update(cart.id, count=count)
        return {"ok": True}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)

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
