
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

# Phase 03의 .env 파일 불러오기
# 위치: practice/phase03/.env
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(env_path)

# PostgreSQL 연결 설정
DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME", "postgres"),
)

# SQLAlchemy Engine 생성
engine = create_engine(DATABASE_URL, echo=True)

# Session 생성 설정
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

# 요청마다 DB Session 제공
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
