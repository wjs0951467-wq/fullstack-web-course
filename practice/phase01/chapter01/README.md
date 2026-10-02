# Chapter 01 학습 기록

- 학습일: 2026-10-02
- 작성자: 전예진
- 실습: Live Server로 첫 웹페이지 실행하고 GitHub에 기록하기

## Browser와 Web Server의 차이

- Browser는 서버에 요청을 보내고, 받은 HTML을 해석해 화면에 보여주는 프로그램이다.
- Web Server는 브라우저의 요청에 응답하여 HTML, CSS, JavaScript 등의 파일을 제공한다.
- 이번 실습에서는 Chrome이 Browser, Live Server가 Web Server 역할을 했다.

예를 들어 Chrome에서 index.html 주소에 접속하면,
Live Server가 HTML을 보내고 Chrome이 제목과 문장을 화면에 표시한다.

## Web Server와 API Server의 차이

| 구분 | 주요 역할 | 예시 |
| --- | --- | --- |
| Web Server | HTML, CSS, JavaScript 등의 파일 제공 | 웹페이지 HTML 전달 |
| API Server | 요청을 처리하고 데이터와 기능 제공 | 회원 정보 조회, 주문 처리 |

Live Server는 이번 실습에서 정적 파일을 제공하는 Web Server이다.
이후 학습할 FastAPI는 API Server를 구현할 때 사용하는 Python 프레임워크이다.

파일 제공과 API 처리는 하나의 서버에서 함께 수행할 수도 있다.

## localhost를 내가 이해한 방식

localhost는 현재 브라우저를 실행하는 내 컴퓨터를 가리키는 이름이다.
127.0.0.1도 내 컴퓨터를 가리키는 루프백 IP 주소이다.

이번 실습 주소:
http://127.0.0.1:5500/practice/phase01/chapter01/index.html

- http: 브라우저와 서버가 통신하는 방식
- 127.0.0.1: 내 컴퓨터
- 5500: Live Server가 요청을 받는 포트 번호
- /practice/phase01/chapter01/index.html: 요청한 파일의 경로

따라서 이 주소는 내 컴퓨터의 5500번 포트에서 실행 중인
Live Server에 index.html을 요청한다는 의미이다.

## Network 탭에서 확인한 GET 요청

개발자 도구의 Network 탭을 연 상태에서 페이지를 새로고침했다.
각 HTML 요청을 선택하고 Headers → General에서 상세 정보를 확인했다.

| 파일 | Request Method | Status Code |
| --- | --- | --- |
| index.html | GET | 304 Not Modified |
| profile.html | GET | 304 Not Modified |

GET은 해당 주소의 자료를 요청하는 HTTP 메서드이다.

304 Not Modified는 요청한 파일이 변경되지 않았으므로
브라우저에 저장된 내용을 사용해도 된다는 응답이다.
오류가 아니라 캐시 재사용과 관련된 정상 응답이다.

## LLM에게 질문한 내용

1. 이번 실습에서도 Python 가상환경을 먼저 만들어야 하는가?
   - HTML과 Live Server만 사용하는 실습이므로 가상환경이 필요 없었다.

2. 어떤 Live Server 확장을 설치해야 하는가?
   - 제작자가 Ritwick Dey인 Live Server 확장을 설치했다.

3. Elements에서 왼쪽 화살표는 무엇인가?
   - HTML 요소 내부를 펼치거나 접는 작은 삼각형이었다.
   - 내 화면에서는 body가 이미 펼쳐져 있었다.

4. Request Method: GET이 보이지 않는 이유는 무엇인가?
   - Headers 상세 영역을 아래로 스크롤한 상태였기 때문이다.
   - 위로 스크롤하면 General에서 확인할 수 있었다.

## 내가 직접 검증한 내용

- 내 계정으로 수업 저장소를 Fork하고 PC에 Clone했다.
- index.html을 작성하고 제목과 본문이 표시되는지 확인했다.
- 처음에는 파일 경로로 페이지를 열었으나, Live Server로 다시 실행했다.
- 주소가 127.0.0.1:5500으로 시작하는지 확인했다.
- Elements 탭에서 h1과 p 요소를 확인했다.
- index.html의 GET 요청과 304 응답을 확인했다.
- profile.html을 작성하고 이름, 학습 과정, 학습 목표 3가지, 완료 문구를 확인했다.
- profile.html의 GET 요청과 304 응답을 확인했다.

### 완료 체크

- [x] Live Server로 페이지 실행
- [x] localhost 또는 127.0.0.1 주소 확인
- [x] Network에서 index.html GET 요청 확인
- [x] profile.html 작성 및 GET 요청 확인
- [x] Browser / Web Server / API Server 차이를 내 말로 설명하기
- [x] Git Commit / Push 완료
- [x] GitHub에서 결과 파일 직접 확인