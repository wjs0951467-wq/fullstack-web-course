
import pytest

from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app.db import engine, get_db
from app.main import app
from app.models import Base


# 테스트 전용 Schema
TEST_SCHEMA = "chapter13_pytest"

# 기존 practice Schema를 테스트 전용으로 변경
test_engine = engine.execution_options(
    schema_translate_map={
        "practice": TEST_SCHEMA,
    }
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    expire_on_commit=False,
)


# 전체 테스트 시작 전 테스트 테이블 준비
@pytest.fixture(scope="session", autouse=True)
def prepare_test_database():
    assert TEST_SCHEMA != "practice"

    with engine.begin() as connection:
        connection.execute(
            text(
                "CREATE SCHEMA IF NOT EXISTS "
                "chapter13_pytest"
            )
        )

    Base.metadata.create_all(bind=test_engine)

    yield

    test_engine.dispose()


# 각 테스트에서 사용할 TestClient
@pytest.fixture
def client():
    # 테스트 전용 테이블만 초기화
    with engine.begin() as connection:
        connection.execute(
            text(
                "TRUNCATE TABLE "
                "chapter13_pytest.members "
                "RESTART IDENTITY"
            )
        )

    # 실제 DB 대신 테스트 DB Session 사용
    def override_get_db():
        db = TestingSessionLocal()

        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
