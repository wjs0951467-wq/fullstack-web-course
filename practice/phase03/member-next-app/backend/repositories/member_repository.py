
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.models import Member
from backend.schemas import MemberUpdate, MemberPatch


# 전체 회원 조회 (GET)
def find_all(db: Session):
    stmt = select(Member).order_by(Member.member_id)
    return db.scalars(stmt).all()


# 회원 ID로 조회 (GET)
def find_by_id(db: Session, member_id: int):
    return db.get(Member, member_id)


# 이메일로 회원 조회
def find_by_email(db: Session, email: str):
    stmt = select(Member).where(Member.email == email)
    return db.scalar(stmt)


# 회원 생성 (POST)
def create_member(db: Session, name: str, email: str, age: int):
    member = Member(name=name, email=email, age=age)

    try:
        db.add(member)
        db.commit()
        db.refresh(member)
        return member

    except IntegrityError:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise


# 회원 전체 수정 (PUT)
def update_member(db: Session, member: Member, payload: MemberUpdate):
    member.name = payload.name
    member.email = str(payload.email)
    member.age = payload.age

    try:
        db.commit()
        db.refresh(member)
        return member

    except Exception:
        db.rollback()
        raise


# 회원 부분 수정 (PATCH)
def patch_member(db: Session, member: Member, payload: MemberPatch):
    changes = payload.model_dump(exclude_unset=True)

    for field, value in changes.items():
        if field == "email":
            value = str(value)

        setattr(member, field, value)

    try:
        db.commit()
        db.refresh(member)
        return member

    except Exception:
        db.rollback()
        raise


# 회원 삭제 (DELETE)
def delete_member(db: Session, member: Member):
    try:
        db.delete(member)
        db.commit()

    except Exception:
        db.rollback()
        raise
