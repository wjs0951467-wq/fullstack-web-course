
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.store_models import (
    Order,
    OrderItem,
    Product,
)


# 주문할 상품 조회 + 행 잠금
def find_products_for_update(
    db: Session,
    product_ids: list[int],
) -> dict[int, Product]:
    stmt = (
        select(Product)
        .where(Product.id.in_(product_ids))
        .order_by(Product.id)
        .with_for_update()
    )

    products = db.scalars(stmt).all()

    return {
        product.id: product
        for product in products
    }


# orders 테이블에 주문 저장
def create_order_record(
    db: Session,
    total_price: int,
) -> Order:
    order = Order(
        total_price=total_price,
        status="created",
    )

    db.add(order)

    # INSERT 실행 후 생성된 주문 ID 확보
    db.flush()

    return order


# order_items 테이블에 주문 상세 저장
def create_order_item_records(
    db: Session,
    order_id: int,
    items: list[tuple[int, int, int]],
) -> None:
    order_items = [
        OrderItem(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
        )
        for product_id, quantity, price in items
    ]

    db.add_all(order_items)
    db.flush()
