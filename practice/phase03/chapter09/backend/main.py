
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.product_router import (
    router as product_router,
)
from backend.routers.order_router import (
    router as order_router,
)


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s %(levelname)s "
        "%(name)s %(message)s"
    ),
)

app = FastAPI(
    title="Chapter 09 - DAY6 Mini Pop-up Store",
    version="1.0.0",
)

# React 3001번 서버 접근 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기존 상품 조회 API
app.include_router(product_router)

# STEP 27: 주문 생성 API
app.include_router(order_router)


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "message": "Chapter 09 API running",
    }
