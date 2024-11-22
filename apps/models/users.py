from enum import Enum

from fastapi_storages import FileSystemStorage
from fastapi_storages.integrations.sqlalchemy import ImageType
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey, BIGINT, BOOLEAN, Enum as SqlEnum
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy_file import ImageField

from apps.models.database import BaseModel


class MainPhoto(BaseModel):
    photo: Mapped[ImageField] = mapped_column(ImageType(storage=FileSystemStorage('media/banner/')))


class User(BaseModel):
    class StatusUser(str, Enum):
        ADMIN = 'admin'
        USER = 'user'
        SELLER = 'seller'
        MODERATOR = 'moderator'

    first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    username: Mapped[str] = mapped_column(String(255))
    lat: Mapped[float] = mapped_column(nullable=True)
    long: Mapped[float] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(SqlEnum(StatusUser), nullable=True)
    contact: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, server_default="False")
    orders: Mapped[list['Order']] = relationship('Order', lazy='selectin', back_populates='order_from_user')
    carts: Mapped[list["Cart"]] = relationship('Cart', lazy='selectin', back_populates='cart_from_user')
    my_shops: Mapped[list["Shop"]] = relationship('Shop', lazy='selectin', back_populates='owner')

    def __str__(self):
        return super().__str__() + f" - {self.username}"


class Cart(BaseModel):
    user_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("users.id", ondelete='CASCADE'))
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("products.id", ondelete='CASCADE'))
    count: Mapped[float] = mapped_column(nullable=True)
    cart_from_user: Mapped[list["Cart"]] = relationship('User', back_populates='carts')


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
    order_items: Mapped[list['OrderItem']] = relationship('OrderItem', lazy='selectin', back_populates='order')
    order_from_user: Mapped['User'] = relationship('User', lazy='selectin', back_populates='orders')


class OrderItem(BaseModel):
    product_id: Mapped[int] = mapped_column(BIGINT, ForeignKey("products.id", ondelete='CASCADE'))
    order_id: Mapped[int] = mapped_column(BIGINT, ForeignKey(Order.id, ondelete='CASCADE'))
    count: Mapped[float] = mapped_column(default=1, nullable=True)
    order: Mapped['Order'] = relationship('Order', lazy='selectin', back_populates='order_items')
