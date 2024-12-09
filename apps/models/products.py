import asyncio

from sqlalchemy import BigInteger, String, VARCHAR, ForeignKey, Integer, CheckConstraint, select, func
from sqlalchemy.orm import mapped_column, Mapped, relationship

from apps.models.database import BaseModel, db


class Category(BaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shops.id', ondelete='CASCADE'), nullable=True)
    parent_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('categories.id', ondelete='CASCADE'), nullable=True)
    icon_name: Mapped[str] = mapped_column(nullable=True)

    def __str__(self):
        if self.parent_id is None:
            return self.name
        return f"{self.parent_id} -> {self.name}"

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
        query = select(cls).filter(cls.shop_id == id_)
        return (await db.execute(query)).scalars().all()

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
    optom_price: Mapped[int] = mapped_column(Integer)
    restorator_price: Mapped[int] = mapped_column(Integer)
    one_price: Mapped[int] = mapped_column(Integer)
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'))
    category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(Category.id, ondelete='CASCADE'))
    photo: Mapped[str] = mapped_column(nullable=True)
    photos: Mapped['ProductPhoto'] = relationship("ProductPhoto", lazy="selectin", back_populates='product')

    __table_args__ = (
        CheckConstraint('one_price > discount_price'),
    )

    @classmethod
    async def get_products_category(cls, category_id):
        query = select(cls).filter(cls.category_id == category_id)
        return (await db.execute(query)).scalars().all()


class ProductPhoto(BaseModel):
    product_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'))
    photo: Mapped[str] = mapped_column(nullable=True)
    product: Mapped['Product'] = relationship("Product", lazy="selectin", back_populates='photos')

    @classmethod
    async def get_products_photos(cls, product_id):
        query = select(cls).filter(cls.product_id == product_id)
        return (await db.execute(query)).scalars().all()
