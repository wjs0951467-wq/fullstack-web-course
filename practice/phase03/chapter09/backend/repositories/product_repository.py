
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.store_models import Product


# 전체 상품 조회 (GET)
def find_all(db: Session) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    return list(db.scalars(stmt).all())
