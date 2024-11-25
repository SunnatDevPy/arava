import asyncio
from enum import Enum

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy import BigInteger, Enum as SqlEnum, String, VARCHAR, ForeignKey, Integer, CheckConstraint, select, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField

from apps.models.database import BaseModel, db
from apps.models.users import User


class Category(BaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shops.id', ondelete='CASCADE'), nullable=True)
    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    photo: Mapped[ImageField] = mapped_column(ImageType(storage=FileSystemStorage('media/category/')))
    parent: Mapped['Category'] = relationship('Category', lazy='selectin', remote_side='Category.id',
                                              back_populates='subcategories')
    products: Mapped[list['Product']] = relationship('Product', lazy='selectin', back_populates='category')
    subcategories: Mapped[list['Category']] = relationship('Category', lazy='selectin', back_populates='parent')
    shop: Mapped[list["Shop"]] = relationship('Shop', lazy='selectin', back_populates='categories')

    def __str__(self):
        if self.parent is None:
            return self.name
        return f"{self.parent} -> {self.name}"

    @classmethod
    async def generate(cls, count: int = 1):
        f = await super().generate(count)
        for _ in range(count):
            await cls.create(
                name=f.company()
            )

    async def async_product_count(self):
        query = select(func.count()).select_from(Product).filter(Product.category_id == self.id)
        return (await db.execute(query)).scalar()

    @classmethod
    async def get_shop_categories(cls, id_):
        query = select(cls).select_from(Category).filter(cls.shop_id == id_)
        return (await db.execute(query)).scalars()

    @property
    def get_products(self):
        # Check if there is an active event loop
        if asyncio.get_event_loop().is_running():
            # If running in an event loop, create a task
            return asyncio.run_coroutine_threadsafe(self.async_product_count(), asyncio.get_event_loop()).result()
        else:
            # If not running in an event loop, use asyncio.run()
            async def inner():
                return await self.async_product_count()

            return self.run_async(inner)


class Product(BaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    discount_price: Mapped[int] = mapped_column(Integer, nullable=True)
    price: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    category: Mapped['Category'] = relationship('Category', lazy='selectin', back_populates='products')

    photos: Mapped[list['ProductPhoto']] = relationship('ProductPhoto', lazy='selectin', back_populates='product')

    __table_args__ = (
        CheckConstraint('price > discount_price'),
    )


class ProductPhoto(BaseModel):
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'))
    product: Mapped['Product'] = relationship('Product', lazy='selectin', back_populates='photos')
    photo: Mapped[ImageField] = mapped_column(ImageType(storage=FileSystemStorage('media/products/')))
