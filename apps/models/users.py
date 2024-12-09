from enum import Enum

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy import Boolean, desc, select, func
from sqlalchemy import ForeignKey, BIGINT, BOOLEAN, Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField

from apps.models.database import BaseModel


class MainPhoto(BaseModel):
    photo: Mapped[str] = mapped_column()


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


class Cart(BaseModel):
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id", ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("products.id", ondelete='CASCADE'))
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
    status: Mapped[str] = mapped_column(SqlEnum(StatusOrder), nullable=True)
    shop_id: Mapped[int] = mapped_column(BIGINT, ForeignKey('shops.id', ondelete="CASCADE"))


class OrderItem(BaseModel):
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("products.id", ondelete='CASCADE'))
    order_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(Order.id, ondelete='CASCADE'))
    count: Mapped[float] = mapped_column(default=1, nullable=True)
