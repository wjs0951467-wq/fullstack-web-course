
# Chapter 05 학습 기록

## 내가 연결한 Database / Schema
- Database: postgres
- 기본 Schema: public
- 실제 조회 Schema: practice
- 조회 테이블: practice.members

## 환경변수를 사용한 이유
- DB 접속 정보를 Python 코드와 분리하기 위해 사용했다.
- 비밀번호가 GitHub에 노출되는 것을 방지하기 위해 .env 파일을 사용했다.
- .gitignore에 .env를 등록하고 Git 제외 여부를 확인했다.

## DB 연결 흐름을 내 말로 설명
1. .env에서 데이터베이스 접속 정보를 가져온다.
2. psycopg를 통해 PostgreSQL에 연결한다.
3. Cursor를 사용해 SQL을 실행한다.
4. fetchone() 또는 fetchall()로 결과를 가져온다.
5. 조회 결과를 Python 데이터로 출력한다.
6. with 문을 사용해 연결과 Cursor를 정리한다.

## 실행한 SELECT
```sql
SELECT current_database(), current_schema();

SELECT member_id, name, email
FROM practice.members
ORDER BY member_id;
```

## 확인한 정상 결과
- Database: postgres
- 기본 Schema: public
- practice.members 테이블에서 회원 4명 조회 성공
- DBeaver와 Python의 조회 결과 일치
- 회원 데이터가 Tuple 형태로 출력됨

## 발생시킨 오류와 원인
1. NameError
   - get_connection() 함수가 정의되지 않아 발생
   - 함수 추가 후 해결

2. OperationalError
   - PostgreSQL 비밀번호가 전달되지 않아 발생
   - .env 설정 확인 및 수정 후 해결

3. SQL Error 42P01
   - members 테이블의 Schema를 지정하지 않아 발생
   - practice.members로 변경하여 해결

4. SQL Error 42703
   - id 컬럼이 존재하지 않아 발생
   - 실제 컬럼명인 member_id로 변경하여 해결

5. ImportError
   - db.py에 fetch_members()가 정의되지 않아 발생
   - db.py에 함수 추가 후 해결

6. Connection refused
   - DB_PORT를 59999로 변경해 연결 오류 재현
   - 5432로 복구한 후 정상 연결 확인

## AI에게 질문한 내용
- NameError와 ImportError의 발생 원인
- PostgreSQL 비밀번호 연결 오류 해결 방법
- Schema와 컬럼명 불일치 문제
- db.py와 main.py의 역할 구분

## 내가 직접 검증한 내용
- .env 파일의 Git 제외 여부
- PostgreSQL Database / Schema 조회
- DBeaver에서 실제 테이블과 컬럼 확인
- Python에서 회원 4명 조회
- 오류 재현 및 정상 복구
