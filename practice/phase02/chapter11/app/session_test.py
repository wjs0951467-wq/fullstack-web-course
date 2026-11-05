
from sqlalchemy import select, func

from app.db import SessionLocal
from app.models import Member


# 1. 기존 회원 확인 및 등록
with SessionLocal() as session:
    email = "orm-test-11@example.com"

    member = session.scalar(
        select(Member).where(Member.email == email)
    )

    if member is None:
        member = Member(
            name="ORM테스트",
            email=email,
            age=25
        )

        session.add(member)
        session.commit()
        session.refresh(member)

        print("회원 등록 성공!")
    else:
        print("기존 회원 조회 성공!")

    print("회원 ID:", member.member_id)
    print("회원 이름:", member.name)
    print("이메일:", member.email)


# 2. 전체 회원 조회
print("\n=== 전체 회원 조회 ===")

with SessionLocal() as session:
    members = session.scalars(select(Member)).all()

    for member in members:
        print(
            member.member_id,
            member.name,
            member.email,
            member.age
        )


# 3. 특정 회원 조회
print("\n=== 회원 ID 1번 조회 ===")

with SessionLocal() as session:
    member = session.scalar(
        select(Member).where(Member.member_id == 1)
    )

    if member:
        print("이름:", member.name)
        print("이메일:", member.email)
        print("나이:", member.age)
    else:
        print("회원이 존재하지 않습니다.")


# 4. execute() 조회
print("\n=== execute() 조회 ===")

with SessionLocal() as session:
    result = session.execute(select(Member))
    row = result.first()

    if row:
        print("execute 결과:", row)
        print("회원 이름:", row[0].name)


# 5. scalars() 조회
print("\n=== scalars() 조회 ===")

with SessionLocal() as session:
    member = session.scalars(select(Member)).first()

    if member:
        print("scalars 결과:", member.name)


# 6. COUNT / SUM 집계 조회
print("\n=== 회원 통계 조회 ===")

with SessionLocal() as session:
    count = session.scalar(
        select(func.count(Member.member_id))
    )

    total_age = session.scalar(
        select(func.sum(Member.age))
    )

    print("전체 회원 수:", count)
    print("회원 나이 합계:", total_age)
