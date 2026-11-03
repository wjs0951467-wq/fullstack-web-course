from fastapi import HTTPException
from chapter10.app.repositories import member_repository


def get_members():
    return member_repository.find_all()


def get_member(member_id: int):
    member = member_repository.find_by_id(member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member


def create_member(data):
    if member_repository.exists_by_email(str(data.email)):
        raise HTTPException(
            status_code=409,
            detail="이미 등록된 이메일입니다."
        )

    return member_repository.create(data)

def update_member(member_id: int, data):
    # 1. 수정할 회원 존재 확인
    if member_repository.find_by_id(member_id) is None:
        raise HTTPException(
            status_code=404,
            detail="회원을 찾을 수 없습니다."
        )

    # 2. 이메일 중복 검사 (자기 자신 제외)
    if member_repository.exists_by_email(
        str(data.email), exclude_member_id=member_id
    ):
        raise HTTPException(
            status_code=409,
            detail="이미 등록된 이메일입니다."
        )

    # 3. 전체 수정
    return member_repository.update(member_id, data)


def patch_member(member_id: int, data):
    # 1. 전달된 필드만 추출
    changes = data.model_dump(exclude_unset=True)

    # 2. 빈 PATCH 요청 검사
    if not changes:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required"
        )

    # 3. 수정할 회원 존재 확인
    if member_repository.find_by_id(member_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    # 4. 이메일 변경 시 중복 검사
    if "email" in changes:
        if member_repository.exists_by_email(
            str(changes["email"]),
            exclude_member_id=member_id
        ):
            raise HTTPException(
                status_code=409,
                detail="이미 등록된 이메일입니다."
            )

    # 5. 일부 필드 수정
    return member_repository.patch(member_id, changes)


def delete_member(member_id: int):
    # 1. 회원 삭제 실행
    deleted = member_repository.delete(member_id)

    # 2. 삭제할 회원이 없으면 404
    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )
