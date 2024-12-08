from sqlalchemy import select, or_
from starlette.requests import Request

from apps.models import Product, Category
from apps.models.products import ProductPhoto
from config import templates

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi import Response
from starlette import status

from apps.models import User, Shop, ShopPhoto

product_router = APIRouter(prefix='/products', tags=['Product'])


# @product_router.post("/")
# async def read_item(request: Request):
#     data = await request.form()
#     await Product.create(**data)
#     return RedirectResponse('/products')


# @product_router.get("/", name='product_list')
# async def get_all_products(request: Request, category: int = None, search: str = None):
#     if category:
#         subquery = select(Category.id).where(or_(Category.parent_id == category, Category.id == category))
#         products = await Product.filter(Product.category_id.in_(subquery))
#     else:
#         products = await Product.all()
#
#     # products = await Product.filter(Product.category_id.in_([1, 2]), columns=(Product, (Product.price * sum_price).label('price_sum')))
#
#     # if search:
#     #     products = await products.filter(or_(Product.name.ilike(f'%{search}%'), Product.description.ilike(f'%{search}%')))
#
#     categories = await Category.filter(Category.parent_id == None, relationship=Category.subcategories)
#
#     context = {
#         'products': products,
#         'categories': categories
#     }
#     return templates.TemplateResponse(request, 'apps/products/product-list.html', context)


@product_router.get(path='', name="Get All Products")
async def list_category_shop():
    products = await Product.all()
    return {"products": products}


@product_router.get(path='/from-shop', name="Get from Shop Products")
async def list_category_shop(shop_id: int):
    categories = await Category.get_shop_categories(shop_id)
    if categories:
        return {'categories': categories}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@product_router.post(path='', name="Create Prdocut from Category")
async def list_category_shop(operator_id: int,
                             category_id: int = Form(default=None),
                             name: str = Form(default=None),
                             price: int = Form(default=None),
                             discount_price: int = Form(default=None),
                             description: str = Form(default=None),
                             ):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin"]:
            await Product.create(description=description, name=name, owner_id=operator_id,
                                 category_id=category_id,
                                 discount_price=discount_price, price=price)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


# Update Shop
@product_router.patch(path='', name="Update Shop")
async def list_category_shop(operator_id: int,
                             shop_id: int = Form(),
                             name: str = Form(default=None),
                             long: float = Form(default=None),
                             lat: float = Form(default=None),
                             shop_category_id: int = Form(default=None),
                             work_time: str = Form(default="CLOSE"),
                             ):
    user = await User.get(operator_id)
    shop = await Shop.get(shop_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user and shop:
        update_data = {k: v for k, v in
                       {"name": name, "shop_category_id": shop_category_id, "photo": photo,
                        "work_time": work_time, "log": long, "lat": lat}.items() if
                       v is not None}

        if user.status.value in ['moderator', "admin"] or user.id == shop.owner_id:
            await Shop.update(shop_id, **update_data)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@product_router.delete(path='', name="Delete Shop")
async def list_category_shop(operator_id: int, shop_id: int):
    user = await User.get(operator_id)
    shop = await Shop.get(shop_id)
    if user and shop:
        if user.status.value in ['moderator', "admin"]:
            await Shop.delete(shop)
            return Response("Item Not Found", status.HTTP_404_NOT_FOUND)
        else:
            return Response("Userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@product_router.get(path='/photos', name="Get Photos Product")
async def list_category_shop(product_id: int):
    products = await Product.get(product_id)
    if products:
        return {'product_photos': products.photos}
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@product_router.post(path='/photos', name="Create Shop Photo")
async def list_category_shop(operator_id: int,
                             product_id: int = Form(),
                             photo: UploadFile = File(default=None),
                             ):
    user = await User.get(operator_id)
    shop = await Product.get(product_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user and shop:
        if user.status.value in ['moderator', "admin"] or user.id == shop.owner_id:
            await ProductPhoto.create(product_id=product_id, photo=photo)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@product_router.patch(path='/photos', name="Update Shop Photo")
async def list_category_shop(operator_id: int,
                             shop_id: int = Form(),
                             shop_photo_id: int = Form(),
                             photo: UploadFile = File(default=None),
                             ):
    user = await User.get(operator_id)
    shop = await ShopPhoto.get(shop_id)
    if not photo.content_type.startswith("image/"):
        return Response("fayl rasim bo'lishi kerak", status.HTTP_404_NOT_FOUND)
    if user and shop:
        update_data = {k: v for k, v in
                       {"photo": photo}.items() if
                       v is not None}
        if user.status.value in ['moderator', "admin"] or user.id == shop.owner_id:
            await ShopPhoto.update(shop_photo_id, **update_data)
            return {"ok": True}
        else:
            return Response("Bu userda xuquq yo'q", status.HTTP_404_NOT_FOUND)
    else:
        return Response("Item Not Found", status.HTTP_404_NOT_FOUND)


@product_router.delete("/photos")
async def user_delete(operator_id: int, shop_photo_id):
    user = await User.get(operator_id)
    if user:
        if user.status.value in ['moderator', "admin"]:
            await ShopPhoto.delete(shop_photo_id)
            return {"ok": True, 'id': shop_photo_id}
        else:
            raise HTTPException(status_code=404, detail="Bu userda xuquq yo'q")
    else:
        raise HTTPException(status_code=404, detail="Item not found")
