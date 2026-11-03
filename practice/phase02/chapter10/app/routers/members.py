
from fastapi import APIRouter, Response, status

from chapter10.app.schemas import (
    MemberCreate,
    MemberCreatedResponse,
    MemberResponse,
    MemberUpdate,
    MemberPatch,
)
from chapter10.app.services import member_service


router = APIRouter(prefix="/members", tags=["members"])


# 전체 회원 조회
@router.get("", response_model=list[MemberResponse])
def get_members():
    return member_service.get_members()


# 특정 회원 조회
@router.get("/{member_id}", response_model=MemberResponse)
def get_member(member_id: int):
    return member_service.get_member(member_id)


# 회원 등록
@router.post(
    "",
    response_model=MemberCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_member(member: MemberCreate):
    return member_service.create_member(member)


# 회원 전체 수정
@router.put("/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member: MemberUpdate):
    return member_service.update_member(member_id, member)


# 회원 부분 수정
@router.patch("/{member_id}", response_model=MemberResponse)
def patch_member(member_id: int, member: MemberPatch):
    return member_service.patch_member(member_id, member)


# 회원 삭제
@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_member(member_id: int):
    member_service.delete_member(member_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
