# Chapter 06 학습 기록

## API Contract
- Method: GET
- URL: /members
- Status: 200 OK
- Response: JSON 배열
- 필드: member_id, name, email

## 사용한 SQL
SELECT member_id, name, email
FROM practice.members
ORDER BY member_id;

## DB에서 확인한 Evidence
- 데이터베이스: postgres
- 스키마: practice
- 회원 수: 4명
- 회원 ID: 1, 2, 3, 4

## Swagger에서 확인한 Evidence
- GET /members 요청 성공
- HTTP Status: 200 OK
- JSON 배열에 회원 4명 반환
- 비밀번호 등 민감정보 없음

## DB와 API 비교
- 회원 수 일치
- 회원 ID 일치
- 이름 및 이메일 일치
- 정렬 순서 일치

## DB Row가 JSON이 되기까지의 흐름

1. Swagger에서 GET /members 요청
2. FastAPI의 get_members() 함수 실행
3. get_connection()으로 PostgreSQL 연결
4. SELECT SQL로 회원 데이터 조회
5. fetchall()로 Python 데이터 가져오기
6. MemberResponse로 응답 데이터 검증
7. JSON 배열로 회원 정보 반환

## 발생한 오류와 실패 지점

### 1. UndefinedColumn
- 원인: 존재하지 않는 member_name 컬럼 조회
- 증상: HTTP 500 Internal Server Error
- 실패 지점: SQL 실행
- 해결: member_name을 name으로 수정

### 2. ResponseValidationError
- 원인: Response Model에 age 필수 필드 추가
- 증상: HTTP 500, 검증 오류 4개
- 실패 지점: 응답 데이터 검증
- 해결: age 필드를 제거하여 응답 형식 일치

## LLM에게 질문하고 확인한 내용

- database.py와 main.py의 역할 구분
- SQL 컬럼 오류의 원인과 발생 위치
- Response Model과 DB 조회 결과의 관계
- 오류 발생 후 최소 수정 방법

## 내가 직접 확인 및 수정한 부분

- database.py와 main.py 코드 분리
- PostgreSQL 데이터베이스 및 스키마 확인
- DBeaver와 Swagger 회원 데이터 비교
- 두 가지 오류 직접 재현
- 오류 원인 확인 후 정상 코드 복구