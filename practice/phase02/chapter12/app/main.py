
from fastapi import FastAPI

from app.routers.member_router import router as member_router


app = FastAPI(
    title="Chapter 12 - SQLAlchemy ORM CRUD",
    description="FastAPI + SQLAlchemy + PostgreSQL",
    version="1.0.0",
)


# 회원 Router 등록
app.include_router(member_router)


# 서버 상태 확인
@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "ok",
        "message": "Chapter 12 ORM API running",
    }
