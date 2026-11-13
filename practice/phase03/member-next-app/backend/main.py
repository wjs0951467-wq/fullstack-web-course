
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routers.member_router import router as member_router


# 기본 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)


# FastAPI 애플리케이션 생성
app = FastAPI(
    title="Chapter 13 - Exception, Logging, TestClient",
    description="FastAPI + SQLAlchemy + Logging + pytest",
    version="1.0.0",
)


# Next.js 프론트엔드 API 요청 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 기존 회원관리 Router 등록
app.include_router(member_router)


# 서버 상태 확인
@app.get("/", tags=["Health"])
def health_check():
    logger.info("Health check requested")

    return {
        "status": "ok",
        "message": "Chapter 13 API running",
    }
