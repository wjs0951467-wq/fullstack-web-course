
from uuid import uuid4


# 테스트용 회원 생성 함수
def create_test_member(client):
    email = f"test-{uuid4().hex}@example.com"

    response = client.post(
        "/members",
        json={
            "name": "Test User",
            "email": email,
            "age": 30,
        },
    )

    assert response.status_code == 201
    return response.json()


# 1. 회원 전체 조회 - 200
def test_get_members_returns_200(client):
    response = client.get("/members")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# 2. 회원 상세 조회 - 200
def test_get_member_returns_200(client):
    member = create_test_member(client)

    response = client.get(
        f"/members/{member['member_id']}"
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Test User"


# 3. 존재하지 않는 회원 - 404
def test_unknown_member_returns_404(client):
    response = client.get("/members/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Member not found"


# 4. 잘못된 회원 ID - 422
def test_invalid_member_id_returns_422(client):
    response = client.get("/members/not-a-number")

    assert response.status_code == 422


# 5. 회원 생성 - 201
def test_create_member_returns_201(client):
    email = f"create-{uuid4().hex}@example.com"

    response = client.post(
        "/members",
        json={
            "name": "Created User",
            "email": email,
            "age": 25,
        },
    )

    assert response.status_code == 201
    assert response.json()["email"] == email


# 6. 중복 이메일 - 409
def test_duplicate_email_returns_409(client):
    member = create_test_member(client)

    response = client.post(
        "/members",
        json={
            "name": "Duplicate User",
            "email": member["email"],
            "age": 31,
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"


# 7. 잘못된 이메일 - 422
def test_invalid_email_returns_422(client):
    response = client.post(
        "/members",
        json={
            "name": "Invalid User",
            "email": "not-an-email",
            "age": 30,
        },
    )

    assert response.status_code == 422


# 8. 빈 PATCH 요청 - 400
def test_empty_patch_returns_400(client):
    member = create_test_member(client)

    response = client.patch(
        f"/members/{member['member_id']}",
        json={},
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "At least one field is required"
    )


# 9. PATCH 정상 수정 - 200
def test_patch_member_returns_200(client):
    member = create_test_member(client)

    response = client.patch(
        f"/members/{member['member_id']}",
        json={"age": 35},
    )

    assert response.status_code == 200
    assert response.json()["age"] == 35


# 10. 없는 회원 PUT - 404
def test_update_unknown_member_returns_404(client):
    response = client.put(
        "/members/999999",
        json={
            "name": "Updated User",
            "email": "updated@example.com",
            "age": 30,
        },
    )

    assert response.status_code == 404


# 11. 없는 회원 PATCH - 404
def test_patch_unknown_member_returns_404(client):
    response = client.patch(
        "/members/999999",
        json={"age": 35},
    )

    assert response.status_code == 404


# 12. 회원 삭제 성공 - 204
def test_delete_member_returns_204(client):
    member = create_test_member(client)

    response = client.delete(
        f"/members/{member['member_id']}"
    )

    assert response.status_code == 204
    assert response.content == b""


# 13. 없는 회원 삭제 - 404
def test_delete_unknown_member_returns_404(client):
    response = client.delete("/members/999999")

    assert response.status_code == 404
