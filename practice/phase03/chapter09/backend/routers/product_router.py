
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.store_schemas import ProductResponse
from backend.services.product_service import get_all_products_service


# DAY6 상품 API Router
router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# 전체 DAY6 상품 조회
@router.get(
    "",
    response_model=list[ProductResponse],
    status_code=200,
)
def get_products(db: Session = Depends(get_db)):
    return get_all_products_service(db)
