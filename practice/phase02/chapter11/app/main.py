
from app.db import engine
from app.models import Base


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("ORM 테이블 준비 완료!")


if __name__ == "__main__":
    create_tables()
