
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas import MemberCreate, MemberUpdate, MemberPatch
from app.repositories import member_repository


# 전체 회원 조회 (GET)
def get_all_members_service(db: Session):
    return member_repository.find_all(db)


# 회원 상세 조회 (GET)
def get_member_service(db: Session, member_id: int):
    member = member_repository.find_by_id(db, member_id)

    if member is None:
        raise HTTPException(
            status_code=404,
            detail="Member not found"
        )

    return member


# 회원 생성 (POST)
def create_member_service(db: Session, payload: MemberCreate):
    existing = member_repository.find_by_email(
        db, str(payload.email)
    )

    if existing is not None:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    try:
        return member_repository.create_member(
            db,
            payload.name,
            str(payload.email),
            payload.age,
        )

    except IntegrityError as exc:
        if getattr(exc.orig, "sqlstate", None) == "23505":
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            ) from exc
        raise


# 회원 전체 수정 (PUT)
def update_member_service(
    db: Session,
    member_id: int,
    payload: MemberUpdate,
):
    member = get_member_service(db, member_id)

    existing = member_repository.find_by_email(
        db, str(payload.email)
    )

    if existing is not None and existing.member_id != member_id:
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    try:
        return member_repository.update_member(db, member, payload)

    except IntegrityError as exc:
        if getattr(exc.orig, "sqlstate", None) == "23505":
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            ) from exc
        raise


# 회원 부분 수정 (PATCH)
def patch_member_service(
    db: Session,
    member_id: int,
    payload: MemberPatch,
):
    member = get_member_service(db, member_id)

    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required"
        )

    if "email" in changes:
        existing = member_repository.find_by_email(
            db, str(changes["email"])
        )

        if existing is not None and existing.member_id != member_id:
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

    try:
        return member_repository.patch_member(db, member, payload)

    except IntegrityError as exc:
        if getattr(exc.orig, "sqlstate", None) == "23505":
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            ) from exc
        raise


# 회원 삭제 (DELETE)
def delete_member_service(db: Session, member_id: int):
    member = get_member_service(db, member_id)
    member_repository.delete_member(db, member)
