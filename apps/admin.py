from typing import Any

from sqladmin import ModelView
from starlette.requests import Request

from apps.models import Product, Category, Order, Cart, User, MainPhoto, OrderItem
from apps.models.products import ProductPhoto


class CategoryAdmin(ModelView, model=Category):
    column_list = ['id', 'name']
    column_details_list = ['id', 'name']
    form_rules = [
        "name",
        "parent"
    ]
    can_export = False
    name_plural = 'Kategoriyalar'
    name = 'Kategoriya'


class ProductAdmin(ModelView, model=Product):
    # column_list = [Product.id, Product.name, Product.photo]
    column_labels = dict(id="ID", name="Nomi", price="Narxi")
    column_formatters = {Product.price: lambda obj, a: f"${obj.price}"}
    column_list = ['id', 'name', 'price']
    column_searchable_list = [Product.name]
    # column_details_exclude_list = ['created_at', 'updated_at']
    # form_excluded_columns = ['created_at', 'updated_at', 'slug', 'owner']
    form_columns = [
        'category',
        'name',
        'discount_price',
        'description',
        'price',
        'currency',
        'owner_id'
    ]
    name_plural = 'Mahsulotlar'
    name = 'Mahsulot'

    # async def insert_model(self, request: Request, data: dict) -> Any:
    #     data['owner_id'] = request.session['user']['id']
    #     return await super().insert_model(request, data)


class ProductPhotoAdmin(ModelView, model=ProductPhoto):
    # column_list = ['id', 'name']
    column_details_list = ['id', 'name']
    # form_rules = [
    #     "name",
    #     "parent"
    # ]
    form_excluded_columns = ['created_at', 'updated_at']
    can_export = False

    # async def insert_model(self, request: Request, data: dict) -> Any:
    #     data['photos'] = request.session['product']['id']
    #     return await super().insert_model(request, data)

    name_plural = 'Mahsulotlarning rasmlari'
    name = 'Rasmlar'


class MainPhotoAdmin(ModelView, model=MainPhoto):
    # column_list = ['id', 'name']
    column_details_list = ['id', 'photo']
    # form_rules = [
    #     "name",
    #     "parent"
    # ]
    form_excluded_columns = ['created_at', 'updated_at']
    can_export = False

    name_plural = 'Bosh menu rasmlar'
    name = 'Bosh menu rasmlar'

    async def after_model_change(self, data: dict, model: Any, is_created: bool, request: Request) -> None:
        return await super().after_model_change(data, model, is_created, request)
