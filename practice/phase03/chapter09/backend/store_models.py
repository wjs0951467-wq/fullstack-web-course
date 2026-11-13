
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from .models import Base


# DAY6 쇼핑몰 전용 PostgreSQL 스키마
STORE_SCHEMA = "mini_popup_store"


# 1. 상품 테이블
class Product(Base):
    __tablename__ = "products"

    __table_args__ = (
        CheckConstraint("price >= 0", name="ck_products_price"),
        CheckConstraint("stock >= 0", name="ck_products_stock"),
        {"schema": STORE_SCHEMA},
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=False),
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )

    stock: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )


# 2. 주문 테이블
class Order(Base):
    __tablename__ = "orders"

    __table_args__ = (
        CheckConstraint(
            "total_price >= 0",
            name="ck_orders_total_price",
        ),
        {"schema": STORE_SCHEMA},
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=False),
        primary_key=True,
    )

    total_price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        server_default="created",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


# 3. 주문 상세 테이블
class OrderItem(Base):
    __tablename__ = "order_items"

    __table_args__ = (
        CheckConstraint(
            "quantity >= 1",
            name="ck_order_items_quantity",
        ),
        CheckConstraint(
            "price >= 0",
            name="ck_order_items_price",
        ),
        {"schema": STORE_SCHEMA},
    )

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=False),
        primary_key=True,
    )

    order_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(f"{STORE_SCHEMA}.orders.id"),
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(f"{STORE_SCHEMA}.products.id"),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    price: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
