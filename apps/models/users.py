from enum import Enum

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy import Boolean, Integer, select, desc
from sqlalchemy import ForeignKey, BIGINT, BOOLEAN, Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy_file import ImageField

from apps.models.database import BaseModel, db


class MainPhoto(BaseModel):
    photo: Mapped[ImageField] = mapped_column(ImageType(storage=FileSystemStorage('media/')))


class BotUser(BaseModel):
    class TypeUser(str, Enum):
        OPTOM = 'optom'
        RESTORATOR = 'restorator'
        ONE = "one"

    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    tg_username: Mapped[str] = mapped_column(String(255), nullable=True)
    lat: Mapped[float] = mapped_column(nullable=True)
    long: Mapped[float] = mapped_column(nullable=True)

    type: Mapped[str] = mapped_column(SqlEnum(TypeUser), nullable=True)
    contact: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="False")

    def __str__(self):
        return super().__str__() + f" - {self.tg_username}"


class AdminPanelUser(BaseModel):
    class StatusUser(str, Enum):
        SUPERUSER = 'superuser'
        ADMIN = 'admin'
        SELLER = 'seller'
        MODERATOR = 'moderator'
        COURIER = 'courier'

    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255), nullable=True)
    password: Mapped[str] = mapped_column(String(255), nullable=True)

    status: Mapped[str] = mapped_column(SqlEnum(StatusUser), nullable=True)
    contact: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="False")

    def __str__(self):
        return super().__str__() + f" - {self.username}"


class MyRestaurant(BaseModel):
    bot_user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("bot_users.id", ondelete='CASCADE'))
    type: Mapped[str] = mapped_column(nullable=True)
    office_name: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str]
    bank_name: Mapped[str]
    xisob_raqami: Mapped[str]
    inn: Mapped[str]
    ndc: Mapped[str] = mapped_column(nullable=True)
    lat: Mapped[float] = mapped_column(nullable=True)
    long: Mapped[float] = mapped_column(nullable=True)

    @classmethod
    async def get_restaurants(cls):
        query = select(cls).order_by(desc(cls.id)).where(cls.type == "restorator")
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def get_optom(cls):
        query = select(cls).order_by(desc(cls.id)).where(cls.type == "optom")
        return (await db.execute(query)).scalars().all()


class MyAddress(BaseModel):
    bot_user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("bot_users.id", ondelete='CASCADE'))
    address: Mapped[str] = mapped_column(String, nullable=True)
    lat: Mapped[float] = mapped_column(nullable=True)
    long: Mapped[float] = mapped_column(nullable=True)


class Cart(BaseModel):
    bot_user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("bot_users.id", ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("shop_products.id", ondelete='CASCADE'))
    shop_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('shops.id', ondelete="CASCADE"))
    count: Mapped[int] = mapped_column(nullable=True)
    shtrix_code: Mapped[int] = mapped_column(BIGINT, nullable=True)


class Order(BaseModel):
    class StatusOrder(str, Enum):
        NEW = "YANGI"
        YIGILMOQDA = "Yig'ilmoqda"
        IN_PROGRESS = "YETKAZILMOQDA"
        DELIVERED = "YETKAZILDI"
        CANCELLED = "BEKOR QILINDI"

    bot_user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('bot_users.id', ondelete='CASCADE'))
    payment: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    payment_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('payments.id', ondelete="CASCADE"))
    payment_name: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(SqlEnum(StatusOrder), nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=True)
    shop_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('shops.id', ondelete="CASCADE"))
    last_first_name: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String)
    driver_price: Mapped[int] = mapped_column(BIGINT)
    total_sum: Mapped[int] = mapped_column(BIGINT, nullable=True)


class OrderItem(BaseModel):
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("shop_products.id", ondelete='CASCADE'))
    order_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(Order.id, ondelete='CASCADE'))
    count: Mapped[float] = mapped_column(default=1, nullable=True)
    price_product: Mapped[int]


class Payment(BaseModel):
    name: Mapped[str] = mapped_column(String)
    status: Mapped[bool] = mapped_column(Boolean)
    token: Mapped[str] = mapped_column(String, nullable=True)


# class PromoCodes(BaseModel):
#     code: Mapped[str] = mapped_column("")

class ProjectAllStatus(BaseModel):
    one_price_protsent: Mapped[int] = mapped_column(Integer)
    optoms_price_protsent: Mapped[int] = mapped_column(Integer)
    optom_price_protsent: Mapped[int] = mapped_column(Integer)
