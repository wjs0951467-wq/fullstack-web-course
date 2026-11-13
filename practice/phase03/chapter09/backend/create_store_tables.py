
from sqlalchemy import inspect, text

from .db import engine
from .store_models import Product, Order, OrderItem, STORE_SCHEMA


def create_store_tables():
    # 이번 실습에서 만들 테이블 3개만 선택
    tables = [
        Product.__table__,
        Order.__table__,
        OrderItem.__table__,
    ]

    # 하나의 트랜잭션에서 스키마와 테이블 생성
    with engine.begin() as conn:
        db_name = conn.scalar(text("SELECT current_database()"))

        print(f"현재 데이터베이스: {db_name}")

        # 기존 실습에서 확인한 DB인지 검증
        if db_name != "postgres":
            raise RuntimeError(
                "예상한 postgres DB가 아닙니다. 작업을 중단합니다."
            )

        # 쇼핑몰 전용 스키마 생성
        conn.execute(
            text(
                "CREATE SCHEMA IF NOT EXISTS mini_popup_store"
            )
        )

        # 기존 회원관리 테이블은 제외하고
        # 쇼핑몰 테이블 3개만 생성
        Product.metadata.create_all(
            bind=conn,
            tables=tables,
            checkfirst=True,
        )

        # 실제 생성 여부 확인
        inspector = inspect(conn)
        created_tables = inspector.get_table_names(
            schema=STORE_SCHEMA
        )

        expected = {"products", "orders", "order_items"}

        for table_name in sorted(expected):
            if table_name not in created_tables:
                raise RuntimeError(
                    f"테이블 생성 실패: {table_name}"
                )

        print("\n생성된 쇼핑몰 테이블:")
        for table_name in sorted(created_tables):
            print(f"- {STORE_SCHEMA}.{table_name}")

    print("\nSTEP 07: 테이블 생성 확인 완료")


if __name__ == "__main__":
    create_store_tables()
