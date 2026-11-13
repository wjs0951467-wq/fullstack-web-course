
from datetime import datetime
from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)


# 기존 STEP 13: 상품 조회 응답
class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    price: int = Field(ge=0)
    category: str
    stock: int = Field(ge=0)


# STEP 27: 주문할 상품 한 종류
class OrderItemCreate(BaseModel):
    product_id: int = Field(gt=0)
    quantity: int = Field(ge=1)


# STEP 27: 주문 생성 요청
class OrderCreate(BaseModel):
    items: list[OrderItemCreate] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_duplicate_products(self) -> Self:
        product_ids = [
            item.product_id
            for item in self.items
        ]

        if len(product_ids) != len(set(product_ids)):
            raise ValueError(
                "같은 상품은 한 번만 입력해야 합니다."
            )

        return self


# STEP 27: 주문 상세 응답
class OrderItemResponse(BaseModel):
    product_id: int
    quantity: int
    price: int = Field(ge=0)


# STEP 27: 주문 생성 결과 응답
class OrderResponse(BaseModel):
    id: int
    total_price: int = Field(ge=0)
    status: str
    created_at: datetime
    items: list[OrderItemResponse]
