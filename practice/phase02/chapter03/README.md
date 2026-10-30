
## POST /members Contract

### Request Body
- name: string, required
- email: string, required
- age: integer, required

### Success
- 201 Created
- created member JSON

### Failure
- invalid body → 422


## Swagger 테스트 결과

### 1. 정상 요청 테스트
- Method: POST
- Request URL: /members
- Request Body: name, email, age 정상 입력
- Response Code: 201 Created
- 결과: 입력한 회원 JSON 정상 반환

### 2. 필수값 누락 테스트
- Method: POST
- Request URL: /members
- Request Body: email 필드 누락
- Response Code: 422
- Error Type: missing
- Error Location: body → email
- 결과: 필수 필드 누락 검증 성공

### 3. 잘못된 데이터 타입 테스트
- Method: POST
- Request URL: /members
- Request Body: age = "not-a-number"
- Response Code: 422
- Error Type: int_parsing
- Error Location: body → age
- 결과: 정수 타입 검증 성공

## 이번 실습에서 배운 점
- Request Body는 클라이언트가 서버로 전달하는 데이터이다.
- Pydantic BaseModel은 입력 데이터의 구조와 타입을 검증한다.
- 올바른 요청은 201을 반환한다.
- 필수값 누락이나 타입 오류는 422를 반환한다.
- 검증에 실패하면 Endpoint 함수가 실행되지 않는다.
