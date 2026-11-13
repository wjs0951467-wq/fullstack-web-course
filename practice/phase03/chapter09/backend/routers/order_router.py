
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from sqlalchemy.orm import Session

from backend.db import get_db
from backend.services.order_service import (
    create_order as create_order_service,
)
from backend.store_schemas import (
    OrderCreate,
    OrderResponse,
)


router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


@router.post(
    "",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
) -> OrderResponse:
    return create_order_service(
        db,
        payload,
    )
