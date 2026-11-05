
# Chapter 11. SQLAlchemy ORM 기초

## 학습 목표
- SQLAlchemy ORM 개념 이해
- Python 클래스와 PostgreSQL 테이블 연결
- DeclarativeBase, Mapped, mapped_column 이해
- Engine과 Session의 역할 이해
- ORM을 이용한 테이블 생성 및 데이터 저장·조회

## 폴더 구조
chapter11/
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   └── session_test.py
└── README.md

## 주요 학습 내용

### 1. ORM Model
- Member 클래스로 members 테이블 정의
- mapped_column으로 컬럼 및 제약조건 설정
- practice 스키마 사용

### 2. Engine
- create_engine()으로 PostgreSQL 연결 설정
- 기존 phase02/.env 환경변수 재사용

### 3. Session
- SessionLocal()로 세션 생성
- session.add()로 객체 등록
- session.commit()으로 변경 사항 확정
- session.refresh()로 DB의 최신 값 조회
- select()로 회원 데이터 조회

## 실행 방법

chapter11 폴더에서 실행

```powershell
python -m app.main
python -m app.session_test
```

## 검증 결과
- [x] SQLAlchemy 설치 및 연결 확인
- [x] ORM 기반 members 테이블 생성
- [x] PostgreSQL practice 스키마 확인
- [x] 회원 데이터 등록 성공
- [x] 기존 회원 조회 성공
- [x] DBeaver에서 데이터 검증 완료

## 핵심 정리
SQLAlchemy ORM을 사용하면 SQL을 직접 작성하지 않고
Python 클래스와 객체를 통해 데이터베이스 작업을 수행할 수 있다.

Engine은 DB 연결을 관리하고,
Session은 데이터 조회 및 변경 작업을 관리한다.
