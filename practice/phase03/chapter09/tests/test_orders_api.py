
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import (
    BigInteger,
    create_engine,
    event,
    select,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from backend.db import get_db
from backend.main import app
from backend.services import order_service
from backend.store_models import Order, OrderItem, Product


# SQLite에서는 BIGINT PRIMARY KEY가 자동 증가하지 않음
# 테스트 환경에서만 INTEGER로 변환
@compiles(BigInteger, "sqlite")
def compile_bigint_sqlite(element, compiler, **kwargs):
    return "INTEGER"


# STEP 28: 주문 전용 테스트 DB
@pytest.fixture
def order_api_client():
    test_engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # PostgreSQL 스키마 구조를 SQLite에 재현
    @event.listens_for(test_engine, "connect")
    def attach_schema(dbapi_connection, connection_record):
        dbapi_connection.execute(
            "ATTACH DATABASE ':memory:' AS mini_popup_store"
        )

    # 실제 DB가 아닌 테스트 DB에 테이블 생성
    with test_engine.begin() as connection:
        Product.__table__.create(bind=connection)
        Order.__table__.create(bind=connection)
        OrderItem.__table__.create(bind=connection)

    # 테스트 상품 2개 준비
    with Session(test_engine) as session:
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
                    stock=1,
                ),
            ]
        )
        session.commit()

    # 실제 PostgreSQL 연결 대신 테스트 DB 제공
    def override_get_db():
        with Session(test_engine) as session:
            yield session

    previous_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            yield client, test_engine

    finally:
        # 테스트가 끝나면 원래 DB 설정 복구
        if previous_override is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = previous_override

        test_engine.dispose()


# TEST 1: 정상 주문 생성
def test_create_order_success(order_api_client):
    client, test_engine = order_api_client

    response = client.post(
        "/orders",
        json={
            "items": [
                {"product_id": 101, "quantity": 2},
                {"product_id": 102, "quantity": 1},
            ]
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] > 0
    assert data["total_price"] == 30000
    assert data["status"] == "created"
    assert len(data["items"]) == 2

    # 응답뿐 아니라 실제 테스트 DB도 확인
    with Session(test_engine) as session:
        orders = session.scalars(select(Order)).all()
        order_items = session.scalars(
            select(OrderItem)
        ).all()

        product_101 = session.get(Product, 101)
        product_102 = session.get(Product, 102)

        assert len(orders) == 1
        assert len(order_items) == 2

        assert orders[0].total_price == 30000

        # 재고 감소 확인
        assert product_101.stock == 8
        assert product_102.stock == 0


# TEST 2: 재고 부족 시 전체 ROLLBACK
def test_order_insufficient_stock_rollback(order_api_client):
    client, test_engine = order_api_client

    # 101번은 정상 수량
    # 102번은 재고 1개인데 2개 주문
    response = client.post(
        "/orders",
        json={
            "items": [
                {"product_id": 101, "quantity": 2},
                {"product_id": 102, "quantity": 2},
            ]
        },
    )

    assert response.status_code == 409

    # 실패한 주문이 DB에 남지 않았는지 확인
    with Session(test_engine) as session:
        orders = session.scalars(select(Order)).all()
        order_items = session.scalars(
            select(OrderItem)
        ).all()

        product_101 = session.get(Product, 101)
        product_102 = session.get(Product, 102)

        assert len(orders) == 0
        assert len(order_items) == 0

        # 앞 상품의 재고도 원래 값 유지
        assert product_101.stock == 10
        assert product_102.stock == 1


# TEST 3: 존재하지 않는 상품 주문
def test_order_product_not_found(order_api_client):
    client, test_engine = order_api_client

    response = client.post(
        "/orders",
        json={
            "items": [
                {"product_id": 999, "quantity": 1}
            ]
        },
    )

    assert response.status_code == 404

    with Session(test_engine) as session:
        assert session.scalars(select(Order)).all() == []
        assert session.scalars(select(OrderItem)).all() == []

        product_101 = session.get(Product, 101)
        assert product_101.stock == 10


# TEST 4: 주문 저장 도중 DB 오류 발생
def test_order_database_error_rollback(
    order_api_client,
    monkeypatch,
):
    client, test_engine = order_api_client

    # 주문 헤더를 저장한 후
    # 주문 상세 저장 단계에서 강제 오류 발생
    def fail_saving_order_items(*args, **kwargs):
        raise SQLAlchemyError(
            "TEST: 주문 상세 저장 실패"
        )

    monkeypatch.setattr(
        order_service,
        "create_order_item_records",
        fail_saving_order_items,
    )

    response = client.post(
        "/orders",
        json={
            "items": [
                {"product_id": 101, "quantity": 2}
            ]
        },
    )

    assert response.status_code == 500

    # 주문 저장이 일부 진행됐더라도 모두 취소
    with Session(test_engine) as session:
        orders = session.scalars(select(Order)).all()
        order_items = session.scalars(
            select(OrderItem)
        ).all()

        product_101 = session.get(Product, 101)

        assert len(orders) == 0
        assert len(order_items) == 0

        # 재고도 원래대로 복구
        assert product_101.stock == 10


# TEST 5: 주문 수량은 반드시 1개 이상
def test_order_invalid_quantity(order_api_client):
    client, test_engine = order_api_client

    response = client.post(
        "/orders",
        json={
            "items": [
                {"product_id": 101, "quantity": 0}
            ]
        },
    )

    assert response.status_code == 422

    with Session(test_engine) as session:
        assert session.scalars(select(Order)).all() == []

        product_101 = session.get(Product, 101)
        assert product_101.stock == 10
