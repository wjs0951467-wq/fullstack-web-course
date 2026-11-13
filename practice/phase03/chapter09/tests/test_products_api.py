
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from backend.main import app
from backend.db import get_db
from backend.store_models import Product


# 테스트용 DB와 API 클라이언트 준비
@pytest.fixture
def api_client():
    # 실제 PostgreSQL 대신 메모리 SQLite 사용
    test_engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # PostgreSQL의 mini_popup_store 스키마를
    # SQLite의 별도 메모리 DB로 재현
    @event.listens_for(test_engine, "connect")
    def attach_schema(dbapi_connection, connection_record):
        dbapi_connection.execute(
            "ATTACH DATABASE ':memory:' AS mini_popup_store"
        )

    # 테스트 상품 테이블만 생성
    with test_engine.begin() as connection:
        Product.__table__.create(bind=connection)

    # 실제 DB 세션 대신 테스트 DB 세션 제공
    def override_get_db():
        with Session(test_engine) as session:
            yield session

    # FastAPI 의존성 주입 교체
    previous_override = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            yield client, test_engine

    finally:
        # 기존 의존성 주입 설정 복구
        if previous_override is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = previous_override

        # 테스트 메모리 DB 정리
        test_engine.dispose()


# TEST 1: 정상 조회와 JSON 배열 검증
def test_get_products_returns_200_and_list(api_client):
    client, test_engine = api_client

    # 테스트 전용 가상 상품
    with Session(test_engine) as session:
        session.add_all([
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
        ])
        session.commit()

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == 2

    # ID 오름차순 정렬 확인
    assert [item["id"] for item in data] == [101, 102]


# TEST 2: 응답 필드와 타입 검증
def test_get_products_response_contract(api_client):
    client, test_engine = api_client

    with Session(test_engine) as session:
        session.add(
            Product(
                id=201,
                name="TEST DAY6 응원봉",
                price=46000,
                category="Fanlight",
                stock=8,
            )
        )
        session.commit()

    response = client.get("/products")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == 1

    product = data[0]

    required_fields = {
        "id",
        "name",
        "price",
        "category",
        "stock",
    }

    assert set(product.keys()) == required_fields

    assert type(product["id"]) is int
    assert type(product["name"]) is str
    assert type(product["price"]) is int
    assert type(product["category"]) is str
    assert type(product["stock"]) is int

    assert product["name"] == "TEST DAY6 응원봉"
    assert product["price"] == 46000
    assert product["stock"] == 8


# TEST 3: 상품이 없는 경우
def test_get_products_empty_list(api_client):
    client, _ = api_client

    response = client.get("/products")

    assert response.status_code == 200
    assert response.json() == []
