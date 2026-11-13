
from sqlalchemy import select, func, text, inspect

from .db import SessionLocal, engine
from .store_models import Product, STORE_SCHEMA


# DAY6 굿즈샵 실습용 샘플 데이터
# 가격은 앞서 정한 예시값, 재고는 가상 수치입니다.
SEED_PRODUCTS = [
    {
        "name": "The DECADE FINALE 트레이딩 카드",
        "price": 5000,
        "category": "Merch",
        "stock": 25,
    },
    {
        "name": "The DECADE FINALE 포토 세트",
        "price": 15000,
        "category": "Merch",
        "stock": 20,
    },
    {
        "name": "데니멀즈 인형 키링 LUCK Ver.",
        "price": 17000,
        "category": "Merch",
        "stock": 15,
    },
    {
        "name": "DAY6 정규 4집 The DECADE",
        "price": 19300,
        "category": "Album",
        "stock": 12,
    },
    {
        "name": "DAY6 OFFICIAL LIGHT BAND VER 3",
        "price": 46000,
        "category": "Fanlight",
        "stock": 8,
    },
    {
        "name": "FOREVER YOUNG 월드투어 Blu-ray",
        "price": 89000,
        "category": "DVD",
        "stock": 0,
    },
]


def seed_products():
    # 실습 DB와 테이블 존재 여부 확인
    with engine.connect() as conn:
        database = conn.scalar(
            text("SELECT current_database()")
        )

        if database != "postgres":
            raise RuntimeError(
                "예상한 실습 DB가 아닙니다."
            )

        tables = inspect(conn).get_table_names(
            schema=STORE_SCHEMA
        )

        if "products" not in tables:
            raise RuntimeError(
                "products 테이블이 없습니다."
            )

    # 기존 상품을 삭제하지 않고 없는 상품만 추가
    with SessionLocal() as session:
        inserted = 0
        skipped = 0

        for data in SEED_PRODUCTS:
            existing_id = session.scalar(
                select(Product.id)
                .where(Product.name == data["name"])
                .limit(1)
            )

            if existing_id is not None:
                skipped += 1
                print(f"SKIP: {data['name']}")
                continue

            session.add(Product(**data))
            inserted += 1
            print(f"ADD: {data['name']}")

        session.commit()

    print(f"\n신규 등록: {inserted}개")
    print(f"기존 상품 유지: {skipped}개")

    # 실제 DB 데이터 재조회
    with SessionLocal() as session:
        products = session.scalars(
            select(Product).order_by(Product.id)
        ).all()

        total = session.scalar(
            select(func.count()).select_from(Product)
        )

        print("\n=== DAY6 상품 조회 ===")

        for product in products:
            print(
                f"{product.id} | "
                f"{product.name} | "
                f"{product.price:,}원 | "
                f"{product.category} | "
                f"재고 {product.stock}"
            )

        print(f"\nDB 전체 상품 수: {total}")


if __name__ == "__main__":
    seed_products()
