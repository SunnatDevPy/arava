import asyncio
from enum import Enum

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy import BigInteger, Enum as SqlEnum, String, VARCHAR, ForeignKey, Integer, CheckConstraint, select, func
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField

from apps.models.database import BaseModel, db
from apps.models import User, Category


class ShopCategory(BaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    shop: Mapped[list['Shop']] = relationship('Shop', lazy='selectin', back_populates='shop_category')


class Shop(BaseModel):
    class WorkTime(str, Enum):
        OPEN = 'open'
        CLOSE = 'close'

    name: Mapped[str] = mapped_column(VARCHAR(255))
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    shop_category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(ShopCategory.id, ondelete='CASCADE'))
    work_time: Mapped[str] = mapped_column(SqlEnum(WorkTime), nullable=True)
    photos: Mapped[ImageField] = mapped_column(ImageType(storage=FileSystemStorage('media/shop/')))
    lat: Mapped[float] = mapped_column(nullable=True)
    long: Mapped[float] = mapped_column(nullable=True)

    shop_category: Mapped['ShopCategory'] = relationship('ShopCategory', lazy='selectin', back_populates='shop')
    shop_photos: Mapped['ShopPhoto'] = relationship('ShopPhoto', lazy='selectin', back_populates='shop')
    owner: Mapped[list["User"]] = relationship('User', lazy='selectin', back_populates='my_shops')
    categories: Mapped[list["Category"]] = relationship('Category', lazy='selectin', back_populates='shop')


class ShopPhoto(BaseModel):
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shops.id', ondelete='CASCADE'))
    shop: Mapped['Shop'] = relationship('Shop', lazy='selectin', back_populates='shop_photos')
    photo: Mapped[ImageField] = mapped_column(ImageType(storage=FileSystemStorage('media/shop/')))

    @classmethod
    async def get_shop_photos(cls, id_):
        query = select(cls).select_from(ShopPhoto).filter(cls.shop_id == id_)
        return (await db.execute(query)).scalars()


# class Languages(BaseModel):
#    name: Mapped[str] =