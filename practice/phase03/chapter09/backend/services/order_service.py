
import logging

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from backend.repositories.order_repository import (
    create_order_item_records,
    create_order_record,
    find_products_for_update,
)
from backend.store_schemas import (
    OrderCreate,
    OrderItemResponse,
    OrderResponse,
)


logger = logging.getLogger(__name__)


def create_order(
    db: Session,
    payload: OrderCreate,
) -> OrderResponse:
    try:
        # 하나의 주문은 하나의 트랜잭션으로 처리
        with db.begin():

            # 1. 주문할 상품의 최신 DB 정보 조회
            product_ids = [
                item.product_id
                for item in payload.items
            ]

            products = find_products_for_update(
                db,
                product_ids,
            )

            total_price = 0

            # (상품 ID, 수량, 주문 당시 단가)
            order_item_rows: list[
                tuple[int, int, int]
            ] = []

            # 2. 상품 존재·재고 확인
            for item in payload.items:
                product = products.get(item.product_id)

                if product is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=(
                            f"상품 ID {item.product_id}번이 "
                            "존재하지 않습니다."
                        ),
                    )

                if product.stock < item.quantity:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=(
                            f"{product.name}: 재고 부족 "
                            f"(현재 {product.stock}개)"
                        ),
                    )

                # 3. 주문 금액 계산
                total_price += (
                    product.price * item.quantity
                )

                # 4. 주문 수량만큼 재고 차감
                product.stock -= item.quantity

                order_item_rows.append(
                    (
                        product.id,
                        item.quantity,
                        product.price,
                    )
                )

            # 5. 주문 생성
            order = create_order_record(
                db,
                total_price,
            )

            # 6. 주문 상세 생성
            create_order_item_records(
                db,
                order.id,
                order_item_rows,
            )

            # 7. 응답 데이터 생성
            result = OrderResponse(
                id=order.id,
                total_price=total_price,
                status=order.status,
                created_at=order.created_at,
                items=[
                    OrderItemResponse(
                        product_id=product_id,
                        quantity=quantity,
                        price=price,
                    )
                    for product_id, quantity, price
                    in order_item_rows
                ],
            )

        # with db.begin() 정상 종료 시 자동 COMMIT
        return result

    except HTTPException:
        # 비즈니스 오류는 원래 HTTP 상태 유지
        # 트랜잭션은 자동 ROLLBACK
        raise

    except SQLAlchemyError:
        logger.exception("주문 DB 저장 실패")

        raise HTTPException(
            status_code=500,
            detail="주문 처리 중 DB 오류가 발생했습니다.",
        )
