from enum import Enum

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy import Boolean, Integer
from sqlalchemy import ForeignKey, BIGINT, BOOLEAN, Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy_file import ImageField

from apps.models.database import BaseModel


class MainPhoto(BaseModel):
    photo: Mapped[ImageField] = mapped_column(ImageType(storage=FileSystemStorage('media/')))


class User(BaseModel):
    class StatusUser(str, Enum):
        SUPERUSER = 'superuser'
        ADMIN = 'admin'
        USER = 'user'
        SELLER = 'seller'
        MODERATOR = 'moderator'
        COURIER = 'courier'

    class TypeUser(str, Enum):
        OPTOM = 'optom'
        RESTORATOR = 'restorator'
        ONE = 'one'

    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255))
    lat: Mapped[float] = mapped_column(nullable=True)
    long: Mapped[float] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(SqlEnum(StatusUser), nullable=True)
    type: Mapped[str] = mapped_column(SqlEnum(TypeUser), nullable=True)
    contact: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="False")

    def __str__(self):
        return super().__str__() + f" - {self.username}"


class MyRestaurant(BaseModel):
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id", ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String, nullable=True)
    lat: Mapped[float] = mapped_column(nullable=True)
    long: Mapped[float] = mapped_column(nullable=True)


class MyAddress(BaseModel):
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id", ondelete='CASCADE'))
    name: Mapped[str] = mapped_column(String, nullable=True)
    lat: Mapped[float] = mapped_column(nullable=True)
    long: Mapped[float] = mapped_column(nullable=True)


class Cart(BaseModel):
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id", ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("shop_products.id", ondelete='CASCADE'))
    shop_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('shops.id', ondelete="CASCADE"))
    count: Mapped[float] = mapped_column(nullable=True)


class Order(BaseModel):
    class StatusOrder(str, Enum):
        NEW = "YANGI"
        PENDING_PAYMENT = "TO'LOV KUTILMOQDA"
        IN_PROGRESS = "YETKAZILMOQDA"
        DELIVERED = "YETKAZILDI"
        CANCELLED = "BEKOR QILINDI"

    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('users.id', ondelete='CASCADE'))
    payment: Mapped[bool] = mapped_column(BOOLEAN, default=False)
    payment_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('payments.id', ondelete="CASCADE"))
    payment_name: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(SqlEnum(StatusOrder), nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=True)
    shop_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('shops.id', ondelete="CASCADE"))
    last_first_name: Mapped[str] = mapped_column(String, nullable=True)
    phone: Mapped[str] = mapped_column(String)
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
