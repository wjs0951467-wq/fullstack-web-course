
import logging

from fastapi import FastAPI

from app.routers.member_router import router as member_router


# Logging 기본 설정
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

logger = logging.getLogger(__name__)


app = FastAPI(
    title="Chapter 13 - Exception, Logging, TestClient",
    description="FastAPI + SQLAlchemy + Logging + pytest",
    version="1.0.0",
)


# 회원 Router 등록
app.include_router(member_router)


# 서버 상태 확인
@app.get("/", tags=["Health"])
def health_check():
    logger.info("Health check requested")

    return {
        "status": "ok",
        "message": "Chapter 13 API running",
    }
