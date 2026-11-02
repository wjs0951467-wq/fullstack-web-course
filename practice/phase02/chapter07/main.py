from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from common.database import get_connection

app = FastAPI()


class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)

class MemberResponse(BaseModel):
    member_id: int
    name: str
    email: str

class MemberCreatedResponse(BaseModel):
    member_id: int
    name: str
    email: str
    age: int



@app.post("/members", response_model=MemberCreatedResponse, status_code=201)
def create_member(member: MemberCreate):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            # 1. 이메일 중복 확인
            cur.execute(
                "SELECT member_id FROM practice.members WHERE email = %s",
                (member.email,)
            )

            if cur.fetchone():
                raise HTTPException(
                    status_code=409,
                    detail="이미 등록된 이메일입니다."
                )

            # 2. 새로운 회원 등록
            cur.execute(
                """
                INSERT INTO practice.members (name, email, age)
                VALUES (%s, %s, %s)
                RETURNING member_id, name, email, age
                """,
                (member.name, member.email, member.age)
            )

            # 3. 등록된 회원 정보 받기
            created = cur.fetchone()

            # 4. DB 저장 확정
            conn.commit()

            return created

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        print(f"DB 오류 발생: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail="회원 등록 중 오류가 발생했습니다."
        )

    finally:
        conn.close()
