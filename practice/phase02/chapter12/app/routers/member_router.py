
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas import (
    MemberCreate,
    MemberUpdate,
    MemberPatch,
    MemberResponse,
    MemberCreatedResponse,
)
from app.services import member_service


router = APIRouter(
    prefix="/members",
    tags=["Members"],
)


# 전체 회원 조회
@router.get("", response_model=list[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    return member_service.get_all_members_service(db)


# 회원 상세 조회
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int, db: Session = Depends(get_db)):
    return member_service.get_member_service(db, member_id)


# 회원 생성
@router.post(
    "",
    response_model=MemberCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(
    payload: MemberCreate,
    db: Session = Depends(get_db),
):
    return member_service.create_member_service(db, payload)


# 회원 전체 수정
@router.put("/{member_id}", response_model=MemberResponse)
def update_member(
    member_id: int,
    payload: MemberUpdate,
    db: Session = Depends(get_db),
):
    return member_service.update_member_service(
        db, member_id, payload
    )


# 회원 부분 수정
@router.patch("/{member_id}", response_model=MemberResponse)
def patch_member(
    member_id: int,
    payload: MemberPatch,
    db: Session = Depends(get_db),
):
    return member_service.patch_member_service(
        db, member_id, payload
    )


# 회원 삭제
@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    member_service.delete_member_service(db, member_id)
