
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import (
    BigInteger,
    create_engine,
    delete,
    event,
)
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from backend.db import get_db
from backend.routers.order_router import (
    router as order_router,
)
from backend.routers.product_router import (
    router as product_router,
)
from backend.store_models import (
    Order,
    OrderItem,
    Product,
)


# STEP 29: 테스트 전용 SQLite 설정
# 기존 PostgreSQL에는 연결하지 않음
@compiles(BigInteger, "sqlite")
def compile_bigint_for_sqlite(
    element,
    compiler,
    **kwargs,
):
    return "INTEGER"


test_engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)


# mini_popup_store 스키마를 메모리 DB에 재현
@event.listens_for(test_engine, "connect")
def attach_test_schema(
    dbapi_connection,
    connection_record,
):
    dbapi_connection.execute(
        "ATTACH DATABASE ':memory:' AS mini_popup_store"
    )


# 테스트 DB에만 테이블 생성
with test_engine.begin() as connection:
    Product.__table__.create(bind=connection)
    Order.__table__.create(bind=connection)
    OrderItem.__table__.create(bind=connection)


# 테스트 전용 상품 데이터
def reset_test_data():
    with Session(test_engine) as session:
        # 외래키 참조 순서를 고려하여 삭제
        session.execute(delete(OrderItem))
        session.execute(delete(Order))
        session.execute(delete(Product))

        session.add_all(
            [
                Product(
                    id=101,
                    name="TEST DAY6 포토카드",
                    price=5000,
                    category="Merch",
                    stock=10,
                ),
                Product(
                    id=102,
                    name="TEST DAY6 앨범",
                    price=20000,
                    category="Album",
                    stock=5,
                ),
            ]
        )

        session.commit()


# 서버 시작 시 테스트 데이터 준비
reset_test_data()


# 실제 FastAPI Router를 사용하는 독립 테스트 앱
app = FastAPI(
    title="Chapter 09 - Isolated Order E2E API",
    version="1.0.0",
)


# 테스트 프론트엔드 3002번만 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3002",
        "http://127.0.0.1:3002",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


# 실제 상품·주문 Router 재사용
app.include_router(product_router)
app.include_router(order_router)


# DB 의존성을 SQLite로 교체
def override_get_db():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# E2E 서버인지 확인하는 전용 API
@app.get("/__e2e__/health")
def e2e_health():
    return {
        "mode": "isolated-sqlite",
        "database": "memory",
        "message": "Test database only",
    }


# E2E 테스트를 반복 실행할 때 데이터 초기화
@app.post("/__e2e__/reset")
def e2e_reset():
    reset_test_data()

    return {
        "mode": "isolated-sqlite",
        "reset": True,
        "products": 2,
    }
