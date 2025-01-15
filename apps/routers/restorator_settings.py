from fastapi import APIRouter, Form, HTTPException
from fastapi import Response
from starlette import status

from apps.models import User, Shop, Cart, PanelProduct
from apps.models.users import MyRestaurant
from apps.utils.details import sum_from_shop, get_shops_unique_cart, detail_cart, get_carts_

cart_router = APIRouter(prefix='/restorator-optom', tags=['Restorator and Optom Settings'])


@cart_router.get(path='', name="All Restaurants and Optoms")
async def list_category_shop():
    res = await MyRestaurant.all()
    return res


@cart_router.get(path='', name="Restaurants and Optoms")
async def list_category_shop():
    return {"optoms": MyRestaurant.get_optom(), "restaurants": MyRestaurant.get_restaurants()}


@cart_router.get(path='/detail', name="Get Restaurant or Optom")
async def list_category_shop(restaurant_id: int):
    restaurant = await MyRestaurant.get(restaurant_id)
    if restaurant:
        return {'restaurant': restaurant}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@cart_router.get(path='/from-user', name="Get Restaurant or Optom address from User")
async def list_category_shop(user_id: int):
    restaurant = await MyRestaurant.get_cart_from_user(user_id)
    return {'restaurant': restaurant}


@cart_router.post(path='', name="Create Restaurant or Optom")
async def list_category_shop(moderator_id: int,
                             user_id: int = Form(),
                             office_name: str = Form(),
                             address: str = Form(),
                             bank_name: str = Form(),
                             xisob_raqami: str = Form(),
                             inn: str = Form(),
                             ndc: str = Form(default=None),
                             lat: float = Form(),
                             long: float = Form()
                             ):
    moderator = await User.get(moderator_id)
    user = await User.get(user_id)
    if user and moderator:
        restaurant = await MyRestaurant.create(user_id=user.id, type=user.type.value, address=address,
                                               bank_name=bank_name,
                                               xisob_raqami=xisob_raqami, inn=inn, ndc=ndc, lat=lat, long=long)
        return {"ok": True, "restaurant": restaurant}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@cart_router.patch(path='', name="Update Restaurant or Optom")
async def list_category_shop(moderator_id: int,
                             restorator_id: int,
                             office_name: str = Form(),
                             address: str = Form(),
                             bank_name: str = Form(),
                             xisob_raqami: str = Form(),
                             inn: str = Form(),
                             ndc: str = Form(default=None),
                             lat: float = Form(),
                             long: float = Form()):
    moderator = await User.get(moderator_id)
    restorator = await MyRestaurant.get(restorator_id)
    if restorator and moderator:
        update_data = {k: v for k, v in
                       {"office_name": office_name,
                        "address": address,
                        "bank_name": bank_name,
                        "xisob_raqami": xisob_raqami,
                        "inn": inn,
                        "ndc": ndc,
                        "lat": lat} if v is not None}
        if moderator.status.value in ['moderator', "admin", "superuser"] or moderator.id == restorator.user_id:
            await MyRestaurant.update(restorator_id, **update_data)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@cart_router.delete("/delete", name="Delete Restaurant or Optom")
async def user_delete(moderator_id: int, restorator_id: int):
    moderator = await User.get(moderator_id)
    restorator = await MyRestaurant.get(restorator_id)
    if restorator and moderator:
        if moderator.status.value in ['moderator', "admin", "superuser"] or moderator.id == restorator.user_id:
            await MyRestaurant.delete(restorator_id)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
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
