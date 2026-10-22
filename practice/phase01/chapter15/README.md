# Member Management — Frontend Mini Project

## 1. 프로젝트 개요

HTML, CSS, JavaScript를 활용하여 회원 목록 조회, 회원 상세 보기, 회원 등록 요청 기능을 구현한 Frontend Basic 개인 프로젝트입니다.

외부 REST API를 사용하여 GET/POST 통신을 연습하고, 사용자 입력부터 API 요청, JSON 응답, DOM 렌더링까지의 데이터 흐름을 이해하는 것을 목표로 합니다.

- **프로젝트:** Member Management
- **학습 과정:** Phase 01 — Frontend Basic / Chapter 15
- **개발 방식:** Vanilla HTML / CSS / JavaScript
- **사용 API:** JSONPlaceholder
- **실행 환경:** VS Code / Live Server / Chrome DevTools
- **제약:** React 및 자체 Backend 미사용, 실제 DB 영구 저장 미구현

## 2. 프로젝트 구조

프로젝트 경로: `practice/phase01/chapter15/`

| 파일 | 역할 |
|---|---|
| `index.html` | 회원 목록, 상세 정보, 등록 Form 화면 구성 |
| `style.css` | 패널 디자인, Grid 레이아웃, 모바일 반응형 |
| `app.js` | API 통신, 데이터 처리, DOM 렌더링, 이벤트 처리 |
| `README.md` | 프로젝트 설명 및 기능 검증 기록 |

## 3. 구현 기능

### 3.1 회원 목록 조회 — GET

- JSONPlaceholder API에서 회원 데이터 조회
- 페이지 실행 시 `loadMembers()` 자동 호출
- JSON 응답을 `members` 배열에 저장
- 회원 이름과 이메일을 버튼 형태로 출력
- 조회된 회원 수 표시

### 3.2 회원 상세 보기

- 회원 목록에서 회원 선택
- 클릭 이벤트를 통해 `renderMemberDetail()` 실행
- 선택한 회원의 이름, 이메일, ID 표시
- `createElement()`와 `textContent`로 DOM 구성

### 3.3 회원 등록 요청 — POST

- 이름과 이메일 입력 Form 제공
- `FormData`로 입력값 수집
- `JSON.stringify()`로 요청 데이터 변환
- `fetch()`를 이용한 POST 요청
- 성공 및 실패 메시지 표시
- 성공 시 Form 입력값 초기화

### 3.4 UI 상태 처리

| 상태 | 처리 내용 |
|---|---|
| Loading | 회원 데이터를 불러오는 중 메시지 |
| Success | 회원 목록 또는 등록 성공 메시지 |
| Empty | 등록된 회원이 없습니다. |
| Error | 회원 정보를 불러오지 못했습니다. |

### 3.5 반응형 디자인

- CSS Grid를 이용한 회원 목록·상세 2열 구성
- 화면 너비 700px 이하에서 1열 전환
- 모바일에서 긴 이메일 줄바꿈 처리
- 입력창 및 버튼 너비 자동 조정

## 4. 전체 시스템 구조

**Browser / Live Server / API Server**

- Browser: HTML, CSS, JavaScript 실행 및 사용자 화면 출력
- Live Server: 정적 파일 제공
- API Server: 회원 데이터 제공 및 POST 요청 처리

외부 API 주소: `https://jsonplaceholder.typicode.com/users`

## 5. 데이터 흐름

### GET — 회원 조회

1. 브라우저에서 페이지 실행
2. `loadMembers()` 호출
3. `fetch(API_URL)`로 GET 요청
4. API 서버에서 JSON 응답 반환
5. 응답을 `members` 배열에 저장
6. `renderMembers()`로 회원 목록 출력
7. 회원 클릭 시 `renderMemberDetail()` 실행

### POST — 회원 등록 요청

1. 사용자가 이름과 이메일 입력
2. Form의 `submit` 이벤트 발생
3. `event.preventDefault()`로 기본 제출 방지
4. `FormData`로 입력값 수집
5. JavaScript 객체 생성
6. `JSON.stringify()`로 JSON 변환
7. `createMember()`에서 POST 요청
8. 서버 응답을 받아 성공 또는 실패 메시지 표시

## 6. 실행 방법

1. VS Code에서 `fullstack-web-course` 프로젝트 열기
2. `practice/phase01/chapter15/index.html` 선택
3. 우클릭 후 **Open with Live Server** 실행
4. 브라우저에서 회원 목록 확인
5. 회원 선택 및 등록 요청 기능 테스트
6. `F12`로 Console / Network 검증

## 7. Network 검증 결과

### 7.1 GET 요청

| 항목 | 검증 결과 |
|---|---|
| Request URL | `https://jsonplaceholder.typicode.com/users` |
| Request Method | GET |
| Status Code | 200 OK |
| Response | 회원 정보를 담은 JSON 배열 |
| 조회 결과 | 총 10명 |
| DOM 렌더링 | 정상 |
| 회원 상세 표시 | 정상 |

초기 검증 과정에서 `304 Not Modified`가 표시되었으며, DevTools의 Disable cache 설정 후 다시 요청하여 `200 OK`를 확인했습니다.

### 7.2 POST 요청

| 항목 | 검증 결과 |
|---|---|
| Request URL | `https://jsonplaceholder.typicode.com/users` |
| Request Method | POST |
| Status Code | 201 Created |
| Request Payload | name, email |
| Response | name, email, id |
| 응답 ID | 11 |
| Console 응답 출력 | 정상 |

등록 요청 성공 메시지와 서버 응답 객체를 확인했습니다.

**주의:** JSONPlaceholder는 테스트용 API이므로 POST 성공이 실제 데이터베이스 영구 저장을 의미하지 않습니다.

## 8. UI 테스트 결과

| 테스트 항목 | 결과 |
|---|---|
| 회원 목록 조회 | 통과 |
| 회원 10명 출력 | 통과 |
| 회원 클릭 및 상세 정보 표시 | 통과 |
| POST 등록 요청 | 통과 |
| POST 응답 확인 | 통과 |
| Empty 상태 | 통과 |
| Error 상태 | 테스트 수행 |
| 모바일 438px 목록·상세 배치 | 통과 |
| 등록 Form 모바일 전체 확인 | 추가 확인 필요 |
| Loading 상태 육안 확인 | 추가 확인 필요 |

## 9. 발생한 문제와 해결 과정

### 9.1 GET 응답에서 304 상태 확인

- 현상: GET 요청에서 `304 Not Modified` 표시
- 원인: 브라우저 캐시 재검증
- 해결: DevTools에서 Disable cache 설정 후 새로고침
- 결과: `200 OK` 응답 확인

### 9.2 Empty 메시지가 유지되지 않는 문제

- 현상: `members = []`로 초기화해도 회원 10명이 다시 표시됨
- 원인: 비동기 GET 요청이 나중에 완료되면서 `members` 배열을 다시 채움
- 해결: 테스트 중 `loadMembers()` 호출을 일시적으로 주석 처리
- 결과: `등록된 회원이 없습니다.` 메시지 확인
- 조치: 테스트 후 임시 코드 삭제 및 정상 동작 복구

### 9.3 Error 상태 테스트

- 잘못된 API 주소를 사용하여 오류 처리 테스트 진행
- `renderError()`를 통한 사용자 오류 안내 흐름 점검
- 테스트 종료 후 정상 API URL로 복구

## 10. AI 활용 및 검증

AI를 활용하여 HTML, CSS, JavaScript 코드를 단계별로 구성하고 코드의 역할을 학습했습니다.

**LLM에 제공한 검증 자료**

- VS Code 코드 스크린샷
- 회원 목록 및 상세 화면
- GET Network Headers / Response
- POST Network Headers / Payload / Response
- Empty 상태 화면
- 모바일 반응형 화면

**직접 수행한 작업**

- 프로젝트 폴더 및 파일 생성
- HTML/CSS/JavaScript 코드 적용
- Live Server 실행 및 기능 테스트
- GET/POST 요청 검증
- 회원 상세 클릭 테스트
- Empty/Error 테스트
- 모바일 반응형 검증

## 11. 학습한 핵심 개념

- HTML: 웹페이지 구조 작성
- CSS: 레이아웃과 반응형 디자인
- DOM: JavaScript로 HTML 요소 제어
- Event: 사용자 행동 감지
- FormData: 입력값 수집
- GET: 서버에서 데이터 조회
- POST: 서버에 데이터 전송
- JSON: 서버와 데이터를 주고받는 형식
- async/await: 비동기 처리
- try/catch: 오류 처리
- DevTools: 실제 요청과 실행 결과 검증

## 12. 향후 확장 방향

Phase 02에서는 직접 Backend 서버를 구현하고 PostgreSQL을 연결하여 실제 데이터 저장 기능을 확장할 수 있습니다.

현재 프로젝트는 **Frontend Basic에서 API 통신 및 UI 상태 처리 흐름을 학습하는 목적**으로 구현했습니다.
