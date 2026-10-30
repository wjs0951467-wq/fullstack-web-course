from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class MemberCreate(BaseModel):
    name: str
    email: str
    age: int

members = [
    {"id": 1, "name": "김원필", "email": "wonpil@example.com", "age": 33},
    {"id": 2, "name": "강영현", "email": "youngk@example.com", "age": 34},
    {"id": 3, "name": "박성진", "email": "sungjin@example.com", "age": 35},
    {"id": 4, "name": "윤도운", "email": "doyun@example.com", "age": 32}
]


@app.get("/members")
def get_members():
    return members


@app.get("/members/{member_id}")
def get_member(member_id: int):
    for member in members:
        if member["id"] == member_id:
            return member

    raise HTTPException(status_code=404, detail="Member not found")


@app.get("/members/search/")
def search_members(name: str | None = None):
    if name is None:
        return members

    keyword = name.lower()

    return [
        member
        for member in members
        if keyword in member["name"].lower()
    ]


@app.get("/members/filter/")
def filter_members(
    name: str | None = None,
    min_age: int | None = None,
):
    result = members

    if name is not None:
        keyword = name.lower()
        result = [
            member
            for member in result
            if keyword in member["name"].lower()
        ]

    if min_age is not None:
        result = [
            member
            for member in result
            if member["age"] >= min_age
        ]

    return result


@app.post("/members", status_code=201)
def create_member(member: MemberCreate):
    return {
        "id": 1,
        "name": member.name,
        "email": member.email,
        "age": member.age,
    }

