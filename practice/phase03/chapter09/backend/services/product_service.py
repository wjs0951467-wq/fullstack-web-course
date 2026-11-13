
import logging

from sqlalchemy.orm import Session

from backend.repositories import product_repository


logger = logging.getLogger(__name__)


# DAY6 전체 상품 조회 Service
def get_all_products_service(db: Session):
    logger.info("Product list requested")

    try:
        return product_repository.find_all(db)

    except Exception:
        logger.exception(
            "Unexpected error while listing products"
        )
        raise
