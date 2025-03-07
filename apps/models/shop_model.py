from enum import Enum

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy import BigInteger, Enum as SqlEnum, VARCHAR, ForeignKey, select, desc, Integer, JSON
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy_file import ImageField

from apps.models.database import BaseModel, db


class MainCategory(BaseModel):
    name: Mapped[str] = mapped_column(VARCHAR(255))
    icon_name: Mapped[str] = mapped_column(nullable=True)


class Shop(BaseModel):
    class WorkTime(str, Enum):
        OPEN = 'open'
        CLOSE = 'close'

    name: Mapped[str] = mapped_column(VARCHAR(255))
    owner_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('admin_panel_users.id', ondelete='CASCADE'), nullable=True)
    main_category_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(MainCategory.id, ondelete='CASCADE'))
    work_status: Mapped[str] = mapped_column(SqlEnum(WorkTime), nullable=True)
    photo: Mapped[ImageField] = mapped_column(ImageType(storage=FileSystemStorage('media/')), nullable=True)
    lat: Mapped[float] = mapped_column(nullable=True)
    long: Mapped[float] = mapped_column(nullable=True)
    group_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    discount_price: Mapped[int] = mapped_column(Integer, nullable=True)
    rating: Mapped[int] = mapped_column(nullable=True)

    @classmethod
    async def get_shops_from_user(cls, id_):
        query = select(cls).order_by(desc(cls.id)).filter(cls.owner_id == id_)
        return (await db.execute(query)).scalars().all()

    # @classmethod
    # async def get_shops_in_category(cls, id_):
    #     query = select(cls).select_from(Shop).filter(cls.id == id_).order_by(desc(cls.id))
    #     return (await db.execute(query)).scalars()

    @classmethod
    async def get_shops_category(cls, id_):
        query = select(cls).select_from(Shop).filter(cls.main_category_id == id_).order_by(desc(cls.id))
        return (await db.execute(query)).scalars().all()


class ShopPhoto(BaseModel):
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shops.id', ondelete='CASCADE'))
    photo: Mapped[ImageField] = mapped_column(ImageType(storage=FileSystemStorage('media/')))

    @classmethod
    async def get_shop_photos(cls, id_):
        query = select(cls).select_from(ShopPhoto).filter(cls.shop_id == id_).order_by(desc(cls.id))
        return (await db.execute(query)).scalars()


class WorkTimes(BaseModel):
    shop_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('shops.id', ondelete='CASCADE'))
    open_time: Mapped[str]
    close_time: Mapped[str]
    weeks: Mapped[list] = mapped_column(JSON)