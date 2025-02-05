from fastapi import APIRouter, File, UploadFile, Form
from fastapi import Response
from pydantic import BaseModel
from starlette import status

from apps.models import PanelProduct, PanelCategory, PanelProductPhoto
from apps.models import AdminPanelUser

panel_product_router = APIRouter(prefix='/panel-products', tags=['Admin Panel Product'])


@panel_product_router.get(path='', name="Get All Products")
async def list_category_shop():
    products = await PanelProduct.all()
    return {"products": products}


@panel_product_router.get(path='/from-category', name="Get Products in Category")
async def list_category_shop(category_id: int):
    products = await PanelCategory.get_products(category_id)
    if products:
        return products
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@panel_product_router.post(path='', name="Create Prdocut from Category")
async def list_category_shop(operator_id: int,
                             category_id: int = Form(default=None),
                             name: str = Form(default=None),
                             shtrix_code: int = Form(),
                             photo: UploadFile = File(default=None),
                             ):
    user = await AdminPanelUser.get(operator_id)
    category = await PanelCategory.get(category_id)
    product = await PanelProduct.get_product_shtrix(shtrix_code)
    if product == None:
        if user and category:
            if user.status.value in ['moderator', "admin", "superuser"]:
                product = await PanelProduct.create(name=name, owner_id=operator_id,
                                                    category_id=category_id,
                                                    photo=photo, shtrix_code=shtrix_code)
                return {"ok": True, "id": product.id}
            else:
                return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Shtrix kodli mahsulot bor", status.HTTP_404_NOT_FOUND)


@panel_product_router.post(path='/photos', name="Create Product")
async def list_category_shop(operator_id: int,
                             product_id: int = Form(),
                             photo: UploadFile = File(default=None),
                             ):
    user = await AdminPanelUser.get(operator_id)
    shop = await PanelProduct.get(product_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user and shop:
        if user.status.value in ['moderator', "admin", "superuser"] or user.id == shop.owner_id:
            object_ = await PanelProductPhoto.create(product_id=product_id, photo=photo)
            return {"ok": True, "id": object_.id}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


class PhotoModel(BaseModel):
    id: int
    photo: str
    product_id: int


@panel_product_router.get(path='/photos', name="Get from Prdoucts Photos")
async def list_category_shop(product_id: int) -> list[PhotoModel]:
    products = await PanelProductPhoto.get_products_photos(product_id)
    return products


@panel_product_router.patch(path='', name="Update Product")
async def list_category_shop(operator_id: int,
                             product_id: int = Form(default=None),
                             name: str = Form(default=None),
                             category_id: float = Form(default=None),
                             shtrix_code: int = Form(default=None),
                             photo: UploadFile = File(default=None)):
    user = await AdminPanelUser.get(operator_id)
    product = await PanelProduct.get(product_id)
    if photo:
        if not photo.content_type.startswith("image/"):
            return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user and product:
        update_data = {k: v for k, v in
                       {"name": name, "category_id": category_id, "photo": photo,
                        "shtrix_code": shtrix_code}.items() if
                       v is not None}

        if user.status.value in ['moderator', "admin", "superuser"]:
            await PanelProduct.update(product_id, **update_data)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@panel_product_router.delete(path='', name="Delete Product")
async def list_category_shop(operator_id: int, product_id: int):
    user = await AdminPanelUser.get(operator_id)
    product = await PanelProduct.get(product_id)
    if user and product:
        if user.status.value in ['moderator', "admin", "superuser"]:
            await PanelProduct.delete(product_id)
            return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


# @panel_product_router.get(path='/photos', name="Get Photos Product")
# async def list_category_shop(product_id: int):
#     products = await Product.get(product_id)
#     if products:
#         return {'product_photos': products.photos}
#     else:
#         return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
#

@panel_product_router.post(path='/photos', name="Create Product Photos")
async def list_category_shop(operator_id: int,
                             product_id: int = Form(),
                             photo: UploadFile = File(default=None),
                             ):
    user = await AdminPanelUser.get(operator_id)
    shop = await PanelProduct.get(product_id)
    if photo:
        if not photo.content_type.startswith("image/"):
            return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user and shop:
        if user.status.value in ['moderator', "admin", "superuser"]:
            photo = await PanelProductPhoto.create(product_id=product_id, photo=photo)
            return {"ok": True, "photo": photo}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@panel_product_router.patch(path='/photos', name="Update Product Photos")
async def list_category_shop(operator_id: int,
                             photo_product_id: int = Form(),
                             photo: UploadFile = File(default=None),
                             ):
    user = await AdminPanelUser.get(operator_id)
    photos = await PanelProduct.get(panel_product_router)
    if photo:
        if not photo.content_type.startswith("image/"):
            return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user and photos:
        update_data = {k: v for k, v in
                       {"photo": photo}.items() if
                       v is not None}
        if user.status.value in ['moderator', "admin", "superuser"]:
            await PanelProduct.update(photo_product_id, **update_data)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@panel_product_router.delete("/photos")
async def user_delete(operator_id: int, product_photo_id: int):
    user = await AdminPanelUser.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin", "superuser"]:
            await PanelProduct.delete(product_photo_id)
            return {"ok": True, 'id': product_photo_id}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
