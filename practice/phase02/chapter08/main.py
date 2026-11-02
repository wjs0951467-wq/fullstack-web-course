from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field, model_validator
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
    age: int

class MemberCreatedResponse(BaseModel):
    member_id: int
    name: str
    email: str
    age: int

class MemberUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


class MemberPatch(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    email: EmailStr | None = None
    age: int | None = Field(default=None, ge=0, le=150)

    @model_validator(mode="after")
    def reject_explicit_null(self):
        for field in self.model_fields_set:
            if getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")
        return self


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

@app.put("/members/{member_id}", response_model=MemberResponse)
def update_member(member_id: int, member: MemberUpdate):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            # 1. 수정할 회원 존재 확인
            cur.execute(
                "SELECT member_id FROM practice.members WHERE member_id = %s",
                (member_id,)
            )

            if cur.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="회원을 찾을 수 없습니다."
                )

            # 2. 이메일 중복 확인 (자기 자신 제외)
            cur.execute(
                """
                SELECT member_id
                FROM practice.members
                WHERE email = %s AND member_id <> %s
                """,
                (str(member.email), member_id)
            )

            if cur.fetchone() is not None:
                raise HTTPException(
                    status_code=409,
                    detail="이미 등록된 이메일입니다."
                )

            # 3. 회원 전체 수정
            cur.execute(
                """
                UPDATE practice.members
                SET name = %s,
                    email = %s,
                    age = %s
                WHERE member_id = %s
                RETURNING member_id, name, email, age
                """,
                (member.name, str(member.email), member.age, member_id)
            )

            updated = cur.fetchone()
            conn.commit()

            return updated

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        print(f"DB 오류 발생: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail="회원 수정 중 오류가 발생했습니다."
        )

    finally:
        conn.close()

        
@app.patch("/members/{member_id}", response_model=MemberResponse)
def patch_member(member_id: int, member: MemberPatch):
    # 1. 실제 전달된 필드만 추출
    changes = member.model_dump(exclude_unset=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="At least one field is required"
        )

    conn = get_connection()

    try:
        with conn.cursor() as cur:
            # 2. 수정할 회원 존재 확인
            cur.execute(
                "SELECT member_id FROM practice.members WHERE member_id = %s",
                (member_id,)
            )

            if cur.fetchone() is None:
                raise HTTPException(
                    status_code=404,
                    detail="Member not found"
                )

            # 3. 이메일 중복 확인
            if "email" in changes:
                cur.execute(
                    """
                    SELECT member_id
                    FROM practice.members
                    WHERE email = %s AND member_id <> %s
                    """,
                    (str(changes["email"]), member_id)
                )

                if cur.fetchone() is not None:
                    raise HTTPException(
                        status_code=409,
                        detail="Email already exists"
                    )

            # 4. 전달된 필드만 UPDATE
            allowed_fields = {
                "name": "name",
                "email": "email",
                "age": "age"
            }

            set_parts = []
            values = []

            for field, value in changes.items():
                column = allowed_fields[field]
                set_parts.append(f"{column} = %s")
                values.append(
                    str(value) if field == "email" else value
                )

            values.append(member_id)

            sql = f"""
                UPDATE practice.members
                SET {', '.join(set_parts)}
                WHERE member_id = %s
                RETURNING member_id, name, email, age
            """

            cur.execute(sql, values)
            updated = cur.fetchone()

            # 5. DB 저장 확정
            conn.commit()

            return updated

    except HTTPException:
        conn.rollback()
        raise

    except Exception as e:
        conn.rollback()
        print(f"DB 오류 발생: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail="회원 수정 중 오류가 발생했습니다."
        )

    finally:
        conn.close()


@app.get("/members/{member_id}", response_model=MemberResponse)
def get_member(member_id: int):
    conn = get_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT member_id, name, email, age
                FROM practice.members
                WHERE member_id = %s
                """,
                (member_id,)
            )

            member = cur.fetchone()

            if member is None:
                raise HTTPException(
                    status_code=404,
                    detail="Member not found"
                )

            return member

    except HTTPException:
        raise

    except Exception as e:
        print(f"DB 오류 발생: {type(e).__name__}: {e}")
        raise HTTPException(
            status_code=500,
            detail="회원 조회 중 오류가 발생했습니다."
        )

    finally:
        conn.close()
