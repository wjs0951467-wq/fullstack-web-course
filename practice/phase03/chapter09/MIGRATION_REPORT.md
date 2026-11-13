# Chapter 09 이전 및 회원관리 원복 보고서

작업일: 2026-11-12 (Asia/Seoul). 브랜치: `main`. 커밋·Push 없음.

## ① 이전 전후 프로젝트 구조

이전 (실제 소스, 의존성·캐시 생략):

```text
practice/phase03/
├── .env                         # 보존, 복사하지 않음
└── member-next-app/
    ├── AGENTS.md
    ├── backend/
    │   ├── main.py              # 회원 + 상품 Router
    │   ├── db.py, models.py, schemas.py, __init__.py
    │   ├── store_models.py, store_schemas.py
    │   ├── create_store_tables.py, seed_store_products.py
    │   ├── repositories/{__init__,member_repository,product_repository}.py
    │   ├── services/{__init__,member_service,product_service}.py
    │   └── routers/{__init__,member_router,product_router}.py
    ├── app/{layout.tsx,page.tsx,globals.css,page.module.css,favicon.ico}
    ├── app/members/{page.tsx,[memberId]/page.tsx}
    ├── app/mini-popup-store/     # 빈 폴더
    ├── components/mini-popup-store/ # 빈 폴더
    ├── components/Member*.tsx
    ├── lib/mini-popup-store/     # 빈 폴더
    ├── lib/members-api.ts
    ├── tests/                   # 빈 폴더
    ├── types/member.ts, public/*.svg
    └── package.json, package-lock.json, tsconfig.json, next.config.ts,
        eslint.config.mjs, .gitignore, .env.local, README.md
```

이후 (실제 소스, 의존성·캐시 생략):

```text
practice/phase03/
├── .env
├── member-next-app/
│   ├── AGENTS.md                # 기존 사용자 파일 보존
│   ├── backend/
│   │   ├── main.py              # 회원 Router만 등록
│   │   ├── db.py, models.py, schemas.py, __init__.py
│   │   ├── repositories/{__init__,member_repository}.py
│   │   ├── services/{__init__,member_service}.py
│   │   └── routers/{__init__,member_router}.py
│   └── 회원관리 프런트엔드 및 설정 파일 보존
└── chapter09/
    ├── MIGRATION_REPORT.md
    ├── backend/
    │   ├── __init__.py
    │   ├── main.py
    │   ├── db.py
    │   ├── models.py            # 독립 DeclarativeBase만 정의
    │   ├── store_models.py
    │   ├── store_schemas.py
    │   ├── create_store_tables.py
    │   ├── seed_store_products.py
    │   ├── repositories/{__init__,product_repository}.py
    │   ├── services/{__init__,product_service}.py
    │   └── routers/{__init__,product_router}.py
    ├── frontend/
    │   ├── .gitignore
    │   ├── AGENTS.md            # next dev 자동 생성
    │   ├── app/layout.tsx
    │   ├── app/page.tsx
    │   ├── app/mini-popup-store/page.tsx # 미구현 상태를 밝힌 임시 페이지
    │   ├── components/mini-popup-store/ # 빈 작업 폴더
    │   ├── lib/mini-popup-store/        # 빈 작업 폴더
    │   ├── package.json
    │   ├── package-lock.json
    │   ├── tsconfig.json
    │   ├── next.config.ts
    │   └── eslint.config.mjs
    └── tests/README.md
```

`frontend/next-env.d.ts`, `node_modules`, `.next`, `tsconfig.tsbuildinfo`는 실행·설치 과정에서 새로 생성된 무시 파일입니다. 기존 프로젝트의 의존성·캐시·Git 메타데이터를 복사하지 않았습니다. 빈 폴더는 Git이 추적하지 않습니다.

## ② 작업한 파일 목록 (절대 경로)

| 구분 | 경로 |
|---|---|
| 기존 코드 이전 (내용 동일) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\store_models.py |
| 기존 코드 이전 (내용 동일) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\store_schemas.py |
| 기존 코드 이전 (내용 동일) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\create_store_tables.py |
| 기존 코드 이전 (내용 동일) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\seed_store_products.py |
| 기존 코드 이전 (내용 동일) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\repositories\product_repository.py |
| 기존 코드 이전 (내용 동일) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\services\product_service.py |
| 기존 코드 이전 (내용 동일) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\routers\product_router.py |
| 경로 변경 (같은 Phase 03 .env 참조, 코드 변경 불필요) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\db.py |
| 기존 코드 이전 (패키지 초기화) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\__init__.py |
| 기존 코드 이전 (패키지 초기화) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\repositories\__init__.py |
| 기존 코드 이전 (패키지 초기화) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\services\__init__.py |
| 기존 코드 이전 (패키지 초기화) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\routers\__init__.py |
| 신규 생성 | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\main.py |
| 신규 생성 (기존 Base 패턴 유지, Member 제외) | C:\dev\fullstack-web-course\practice\phase03\chapter09\backend\models.py |
| 기존 코드 이전 (프로젝트 이름만 변경) | C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend\package.json |
| 기존 코드 이전 (프로젝트 이름만 변경) | C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend\package-lock.json |
| 기존 코드 이전 | C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend\tsconfig.json |
| 기존 코드 이전 | C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend\next.config.ts |
| 기존 코드 이전 | C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend\eslint.config.mjs |
| 기존 코드 이전 | C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend\.gitignore |
| 신규 생성 (Next.js 자동 생성) | C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend\AGENTS.md |
| 신규 생성 | C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend\app\layout.tsx |
| 신규 생성 | C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend\app\page.tsx |
| 신규 생성 (임시 페이지) | C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend\app\mini-popup-store\page.tsx |
| 신규 생성 | C:\dev\fullstack-web-course\practice\phase03\chapter09\tests\README.md |
| 신규 생성 | C:\dev\fullstack-web-course\practice\phase03\chapter09\MIGRATION_REPORT.md |
| 기존 파일 원복 (상품 Router import/등록만 제거) | C:\dev\fullstack-web-course\practice\phase03\member-next-app\backend\main.py |
| 기존 파일 원복 (HEAD와 내용 동일) | C:\dev\fullstack-web-course\practice\phase03\member-next-app\package.json |
| 기존 파일 원복 (HEAD와 내용 동일) | C:\dev\fullstack-web-course\practice\phase03\member-next-app\package-lock.json |
| 변경 없음 | C:\dev\fullstack-web-course\practice\phase03\member-next-app\AGENTS.md |
| 변경 없음 | C:\dev\fullstack-web-course\practice\phase03\.env |
| 변경 없음 | C:\dev\fullstack-web-course\practice\phase03\member-next-app\.env.local |

위 7개 쇼핑몰 전용 Python 원본은 바이트 일치·DB·HTTP 검증 후에만 제거했습니다. `member-next-app/backend`의 기존 `__init__.py`, `db.py`, `models.py`, `schemas.py`, `member_*` 파일은 보존했습니다. 기존 회원관리 app/components/lib/types/public 소스도 변경하지 않았습니다.

로컬 안전 백업: `C:\dev\fullstack-web-course\.migration-backup-ch09\`. 자체 `.gitignore`의 `*`로 Git에서 제외됩니다. 변경 전 main/package/lock/AGENTS, 이동한 7개 원본, 비밀정보 없는 DB 해시·상품 스냅샷, 작업용 검증 스크립트를 보관했습니다. `.env`와 비밀정보는 백업하지 않았습니다. 검증 스크립트는 이번 이전의 진단 도구이며 STEP 14 테스트 구현이 아닙니다.

## ③ 기존 회원관리 원복 결과

- 상품 Router import 및 등록 블록만 제거했습니다. 회원 Router, CORS 3000, 로깅 동작, Health Check는 유지했습니다.
- Git diff에 남은 main.py 변경은 기존 사용자의 주석 수정 3개입니다. 임의로 HEAD로 덮어쓰지 않았습니다.
- package/lock의 추가 변경은 Playwright 의존성뿐임을 확인한 후 HEAD 내용으로 복구했습니다. `npm.cmd prune --offline --no-audit --no-fund`로 원본의 불필요한 Playwright 3개 설치 패키지도 제거했습니다.
- 기존 `AGENTS.md`는 미추적 사용자 파일로 계속 보존했습니다.
- 최종 Git 내용 diff는 main.py의 주석 3개뿐이며, 신규 소스는 chapter09 전체입니다. `git status --short`에는 package.json이 M으로 남아 있지만 package/lock의 `git diff`는 모두 비어 있습니다 (줄바꿈/인덱스 상태 표시). 원래 패키지 선언 내용은 복구되었습니다.
- 비어 있던 app/components/lib의 mini-popup-store 및 tests 폴더만 제거했습니다. 이전할 쇼핑몰 테스트 파일은 없었습니다.
- 회원 GET 목록·상세 HTTP 200, POST/PUT/PATCH/DELETE 등록을 확인했습니다. 쓰기 요청은 데이터 보존을 위해 실행하지 않았습니다.

## ④ PostgreSQL 보존 결과

동일한 `practice/phase03/.env`와 기존 SQLAlchemy SessionLocal 패턴을 사용했습니다. backend/db.py의 `Path(__file__).resolve().parents[2]`는 새 위치에서도 Phase 03을 가리킵니다. Python import는 `chapter09`를 작업 디렉터리로 하여 기존 `backend.*` 경로를 그대로 사용합니다. 회원관리 Backend에 의존하지 않습니다.

읽기 전용 트랜잭션으로 이전 전후 전체 행·제약조건을 비교했습니다.

| DB | 테이블 | 이전/이후 행 수 | 비교 |
|---|---|---:|---|
| postgres | mini_popup_store.products | 6 / 6 | 모든 필드 동일 |
| postgres | mini_popup_store.orders | 0 / 0 | 동일 |
| postgres | mini_popup_store.order_items | 0 / 0 | 동일 |
| postgres | practice.members | 6 / 6 | 모든 필드 해시 동일 |

쇼핑몰 PK/FK/CHECK 정의도 전체 일치했습니다. CREATE/Seed 실행, DROP/TRUNCATE/DELETE, 데이터 변경은 수행하지 않았습니다.

| ID | 상품명 | 가격 | 카테고리 | 재고 |
|---|---|---:|---|---:|
| 1 | The DECADE FINALE 트레이딩 카드 | 5000 | Merch | 25 |
| 2 | The DECADE FINALE 포토 세트 | 15000 | Merch | 20 |
| 3 | 데니멀즈 인형 키링 LUCK Ver. | 17000 | Merch | 15 |
| 4 | DAY6 정규 4집 The DECADE | 19300 | Album | 12 |
| 5 | DAY6 OFFICIAL LIGHT BAND VER 3 | 46000 | Fanlight | 8 |
| 6 | FOREVER YOUNG 월드투어 Blu-ray | 89000 | DVD | 0 |

products 전체 행 SHA-256 (이전/이후 동일): `fc8b589b3a97b951ac5a385cdf7a0ad3efe2630afb24671026ed622612417667`.

## ⑤ 실제 실행 테스트 결과

아래 명령은 지정 프로젝트 디렉터리에서 실행했습니다. `verify.py` 명령의 작업 디렉터리는 저장소 루트입니다.

| 상태 | 명령/검사 | 실제 결과 |
|---|---|---|
| PASS | `.\.venv\Scripts\python.exe .migration-backup-ch09/verify.py baseline` | postgres, 기존 3개 쇼핑몰 테이블, 상품 6개 스냅샷 확보 |
| PASS | `.\.venv\Scripts\python.exe .migration-backup-ch09/verify.py chapter` | Python 모듈 import, Base 메타데이터 쇼핑몰 3개만 등록, Repository/Service 각 6개 |
| PASS | 위 chapter 진단 내 Uvicorn 실제 서버 (8001) 및 HTTP GET | /products 200, JSON 배열 6개, id/name/price/category/stock 전체 값 DB와 일치 |
| PASS | 위 chapter 진단 내 OPTIONS /products | Origin http://localhost:3001 허용 확인 |
| PASS | `.\.venv\Scripts\python.exe .migration-backup-ch09/verify.py member` | 회원 CRUD OpenAPI 유지, 실제 /members 및 /members/1 HTTP 200 |
| PASS | 정리 후 chapter 및 member 진단 재실행 | 4개 테이블 전체 행 해시 및 쇼핑몰 제약조건 이전 스냅샷과 동일 |
| PASS | Chapter frontend: `npm.cmd ci --offline --no-audit --no-fund` | 347개 패키지 독립 설치, 기존 node_modules 복사 없음 |
| PASS | Chapter frontend: `npm.cmd ls --depth=0` | Next 16.4.6, React 19.3.0, Playwright 1.65.0 설치 확인 |
| PASS | Chapter frontend: `npm.cmd run build` | / 및 /mini-popup-store 정적 빌드 성공 |
| PASS | Chapter frontend: `npm.cmd run lint` | ESLint 오류 없음 |
| PASS | Chapter frontend: `node node_modules/typescript/bin/tsc --noEmit` | 타입 오류 없음 |
| PASS | Chapter frontend: `npm.cmd run dev -- --hostname 127.0.0.1 --port 3001` | Ready, 임시 페이지 개발 서버 구동 |
| PASS | `Invoke-WebRequest -UseBasicParsing http://127.0.0.1:3001/mini-popup-store` | HTTP 200 |
| FAIL → PASS | Member frontend: `npm.cmd run build` | 첫 시도 Google Fonts 네트워크 실패, 권한 확장 후 같은 명령으로 정상 빌드. 회원 /members 및 /members/[memberId] 유지 |
| PASS | Member frontend: `npm.cmd run lint` | 오류 없음 |
| PASS | Member frontend: `node node_modules/typescript/bin/tsc --noEmit` | 오류 없음 |
| PASS | Member frontend: `npm.cmd ls --depth=0` (prune 후) | 원래 의존성 유지, extraneous Playwright 없음 |
| PASS | `git diff --check` | 공백 오류 없음 |
| HOLD | STEP 14 pytest / 이후 Playwright 시나리오 | 미작성·미실행, 완료 처리하지 않음 |
| HOLD | 회원 쓰기 API 실제 변경 테스트 | 등록만 검증, POST/PUT/PATCH/DELETE 요청은 미실행 |

Python은 기존 `.venv`를 사용했습니다. 샌드박스에서 Python 본체 접근이 제한되어 권한 확장 실행으로 검증했습니다. 보안 정책 변경 없이 `PSYCOPG_IMPL=python`과 기존 PostgreSQL 18 bin 경로만 프로세스에 설정했습니다. 프런트엔드는 아직 상품 API를 호출하는 코드를 구현하지 않았으므로 API URL 환경변수나 Secret 복사도 없습니다. 사용 API 주소는 `http://localhost:8001/products`, CORS 프런트엔드 포트는 3001입니다.

검증용 서버는 종료했습니다. 사용자 기존 서버는 종료하지 않았습니다.

## ⑥ 이후 강의 진행 위치

STEP 13의 실제 GET /products 응답 검증까지 완료했습니다. 다음 진행 위치는 **STEP 14**입니다. 상품 카드·장바구니·주문 UI 및 이후 기능은 구현하지 않았습니다.

## ⑦ 최종 실행 명령어 (Windows PowerShell)

터미널 1 — Chapter 09 FastAPI:

```powershell
Set-Location C:\dev\fullstack-web-course\practice\phase03\chapter09
$env:PSYCOPG_IMPL = "python"
$env:Path = "C:\Program Files\PostgreSQL\18\bin;$env:Path"
& C:\dev\fullstack-web-course\.venv\Scripts\python.exe -m uvicorn backend.main:app --reload --port 8001
```

Swagger: http://localhost:8001/docs

터미널 2 — Chapter 09 Next.js:

```powershell
Set-Location C:\dev\fullstack-web-course\practice\phase03\chapter09\frontend
npm.cmd run dev -- --port 3001
```

임시 페이지: http://localhost:3001/mini-popup-store

현재 의존성은 설치 완료 상태입니다. 다른 환경에서 새로 설치할 때는 같은 frontend 폴더에서 `npm.cmd ci`를 먼저 실행합니다. PowerShell 실행 정책에 막힌 npm.ps1 대신 npm.cmd를 사용합니다.
