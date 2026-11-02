# Chapter 08. PUT/PATCH + UPDATE

## 1. 학습 목표

- PUT과 PATCH의 차이 이해
- Pydantic을 이용한 전체 수정 및 부분 수정 Schema 구현
- PostgreSQL UPDATE와 RETURNING 활용
- Parameterized Query를 통한 안전한 데이터 수정
- HTTP 상태 코드 400 / 404 / 409 / 422 구분
- Swagger, PostgreSQL, GET 재조회를 통한 수정 결과 검증

## 2. 구현 내용

### PUT /members/{member_id}

회원의 이름, 이메일, 나이를 전체 수정하는 API 구현

- MemberUpdate Schema 적용
- 수정 대상 회원 존재 여부 확인
- 자기 자신을 제외한 이메일 중복 검사
- UPDATE ... RETURNING으로 수정된 정보 반환
- commit(), rollback()으로 트랜잭션 처리

### PATCH /members/{member_id}

요청에 포함된 필드만 수정하는 API 구현

- MemberPatch Schema 적용
- model_dump(exclude_unset=True) 활용
- 필드 생략과 명시적 null 구분
- 허용된 컬럼만 동적 UPDATE
- 수정되지 않은 필드는 기존 값 유지

### GET /members/{member_id}

수정된 회원 정보를 재조회하기 위한 API 구현

## 3. 실습 검증 결과

| 테스트 | 결과 |
|---|---|
| PUT 전체 수정 | DB 반영 성공 |
| PUT 필수 필드 누락 | 422 |
| PATCH 나이만 수정 | 200 |
| PATCH 빈 요청 | 400 |
| PATCH 존재하지 않는 회원 | 404 |
| PATCH 이메일 중복 | 409 |
| PATCH 명시적 null | 422 |
| GET 재조회 | 200 |
| PostgreSQL 데이터 비교 | 일치 |

### 검증 데이터

- member_id: 7
- name: PUT수정테스트
- email: chapter08-put-7@example.com
- age: 29 → 31

PATCH 요청으로 나이만 변경한 후 Swagger 응답, PostgreSQL 데이터, GET 재조회 결과가 모두 일치함을 확인했다.

## 4. 핵심 학습 내용

- PUT은 수정 가능한 전체 필드를 전달해야 한다.
- PATCH는 변경할 필드만 전달할 수 있다.
- exclude_unset=True는 생략된 필드를 제외한다.
- 명시적 null은 별도 검증이 필요하다.
- SQL 값은 %s 파라미터로 안전하게 전달한다.
- UPDATE 이후 commit()을 수행해야 수정 결과가 저장된다.

## 5. 학습 정리

이번 실습을 통해 FastAPI에서 회원 수정 API를 구현하고 PostgreSQL 데이터가 실제로 변경되는 과정을 확인했다.

특히 PUT과 PATCH의 차이, Pydantic Validation, HTTP 오류 처리, 데이터베이스 수정 결과를 검증하는 방법을 학습했다.