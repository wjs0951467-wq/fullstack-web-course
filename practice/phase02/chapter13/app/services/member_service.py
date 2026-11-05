
import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.schemas import MemberCreate, MemberUpdate, MemberPatch
from app.repositories import member_repository


logger = logging.getLogger(__name__)


# 전체 회원 조회 (GET)
def get_all_members_service(db: Session):
    logger.info("Member list requested")

    try:
        return member_repository.find_all(db)
    except Exception:
        logger.exception("Unexpected error while listing members")
        raise


# 회원 상세 조회 (GET)
def get_member_service(db: Session, member_id: int):
    logger.info("Member lookup started: member_id=%s", member_id)

    try:
        member = member_repository.find_by_id(db, member_id)
    except Exception:
        logger.exception("Unexpected error during member lookup")
        raise

    if member is None:
        logger.warning(
            "Member not found: member_id=%s",
            member_id,
        )
        raise HTTPException(
            status_code=404,
            detail="Member not found",
        )

    logger.info("Member lookup succeeded: member_id=%s", member_id)
    return member


# 회원 생성 (POST)
def create_member_service(db: Session, payload: MemberCreate):
    logger.info("Member creation started")

    try:
        existing = member_repository.find_by_email(
            db, str(payload.email)
        )

        if existing is not None:
            logger.warning("Duplicate member email detected")
            raise HTTPException(
                status_code=409,
                detail="Email already exists",
            )

        member = member_repository.create_member(
            db,
            payload.name,
            str(payload.email),
            payload.age,
        )

        logger.info(
            "Member created: member_id=%s",
            member.member_id,
        )
        return member

    except HTTPException:
        raise

    except IntegrityError as exc:
        if getattr(exc.orig, "sqlstate", None) == "23505":
            logger.warning("Duplicate email constraint violation")
            raise HTTPException(
                status_code=409,
                detail="Email already exists",
            ) from exc

        logger.exception("Unexpected integrity error creating member")
        raise

    except Exception:
        logger.exception("Unexpected error while creating member")
        raise


# 회원 전체 수정 (PUT)
def update_member_service(
    db: Session,
    member_id: int,
    payload: MemberUpdate,
):
    logger.info("Member update started: member_id=%s", member_id)

    member = get_member_service(db, member_id)

    try:
        existing = member_repository.find_by_email(
            db, str(payload.email)
        )

        if existing is not None and existing.member_id != member_id:
            logger.warning("Duplicate email during member update")
            raise HTTPException(
                status_code=409,
                detail="Email already exists",
            )

        updated = member_repository.update_member(
            db, member, payload
        )

        logger.info("Member updated: member_id=%s", member_id)
        return updated

    except HTTPException:
        raise

    except IntegrityError as exc:
        if getattr(exc.orig, "sqlstate", None) == "23505":
            logger.warning("Duplicate email constraint violation")
            raise HTTPException(
                status_code=409,
                detail="Email already exists",
            ) from exc

        logger.exception("Unexpected integrity error updating member")
        raise

    except Exception:
        logger.exception("Unexpected error while updating member")
        raise


# 회원 부분 수정 (PATCH)
def patch_member_service(
    db: Session,
    member_id: int,
    payload: MemberPatch,
):
    logger.info("Member patch started: member_id=%s", member_id)

    member = get_member_service(db, member_id)
    changes = payload.model_dump(exclude_unset=True)

    if not changes:
        logger.warning("Empty PATCH request: member_id=%s", member_id)
        raise HTTPException(
            status_code=400,
            detail="At least one field is required",
        )

    try:
        if "email" in changes:
            existing = member_repository.find_by_email(
                db, str(changes["email"])
            )

            if existing is not None and existing.member_id != member_id:
                logger.warning("Duplicate email during member patch")
                raise HTTPException(
                    status_code=409,
                    detail="Email already exists",
                )

        updated = member_repository.patch_member(
            db, member, payload
        )

        logger.info("Member patched: member_id=%s", member_id)
        return updated

    except HTTPException:
        raise

    except IntegrityError as exc:
        if getattr(exc.orig, "sqlstate", None) == "23505":
            logger.warning("Duplicate email constraint violation")
            raise HTTPException(
                status_code=409,
                detail="Email already exists",
            ) from exc

        logger.exception("Unexpected integrity error patching member")
        raise

    except Exception:
        logger.exception("Unexpected error while patching member")
        raise


# 회원 삭제 (DELETE)
def delete_member_service(db: Session, member_id: int):
    logger.info("Member deletion started: member_id=%s", member_id)

    member = get_member_service(db, member_id)

    try:
        member_repository.delete_member(db, member)
        logger.info("Member deleted: member_id=%s", member_id)

    except Exception:
        logger.exception("Unexpected error while deleting member")
        raise
