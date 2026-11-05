
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict,
    model_validator,
)


# 회원 생성 (POST)
class MemberCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


# 회원 전체 수정 (PUT)
class MemberUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)


# 회원 부분 수정 (PATCH)
class MemberPatch(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    email: EmailStr | None = None
    age: int | None = Field(
        default=None,
        ge=0,
        le=150,
    )

    @model_validator(mode="before")
    @classmethod
    def reject_null(cls, data):
        if isinstance(data, dict):
            for field in ("name", "email", "age"):
                if field in data and data[field] is None:
                    raise ValueError(f"{field} cannot be null")
        return data


# 회원 조회 응답
class MemberResponse(BaseModel):
    member_id: int
    name: str
    email: str
    age: int

    model_config = ConfigDict(from_attributes=True)


# 회원 생성 응답
class MemberCreatedResponse(MemberResponse):
    pass
