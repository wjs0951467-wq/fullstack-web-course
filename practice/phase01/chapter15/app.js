
/* ==================================
   1. API 주소 및 DOM 요소 선택
================================== */

const API_URL = "https://jsonplaceholder.typicode.com/users";

const memberList = document.querySelector("#member-list");
const memberDetail = document.querySelector("#member-detail");
const memberForm = document.querySelector("#member-form");
const statusBox = document.querySelector("#status");
const formMessage = document.querySelector("#form-message");

// 회원 데이터를 저장할 배열
let members = [];


/* ==================================
   2. Loading 상태 처리
================================== */

function renderLoading() {
    statusBox.textContent = "불러오는 중...";
    memberList.replaceChildren();
}


/* ==================================
   3. Error 상태 처리
================================== */

function renderError(message) {
    statusBox.textContent = message;
    memberList.replaceChildren();
}


/* ==================================
   4. Empty 상태 처리
================================== */

function renderEmpty() {
    statusBox.textContent = "등록된 회원이 없습니다.";
    memberList.replaceChildren();
}


/* ==================================
   5. 회원 상세 정보 표시
================================== */

function renderMemberDetail(member) {
    // 기존 상세 정보 삭제
    memberDetail.replaceChildren();

    // 회원 이름
    const name = document.createElement("h3");
    name.textContent = member.name ?? "-";

    // 회원 이메일
    const email = document.createElement("p");
    email.textContent = member.email ?? "-";

    // 회원 ID
    const id = document.createElement("p");
    id.textContent = `ID: ${member.id ?? "-"}`;

    // 상세 정보 화면에 추가
    memberDetail.append(name, email, id);
}


/* ==================================
   6. 회원 목록 렌더링
================================== */

function renderMembers() {
    // 기존 회원 목록 삭제
    memberList.replaceChildren();

    // 회원이 없으면 Empty 처리
    if (members.length === 0) {
        renderEmpty();
        return;
    }

    // 회원 수 표시
    statusBox.textContent = `총 ${members.length}명`;

    // 회원 배열 반복
    members.forEach(function (member) {
        // 회원 버튼 생성
        const button = document.createElement("button");

        button.type = "button";
        button.className = "member-card";

        // 이름 및 이메일 표시
        button.textContent =
            `${member.name ?? "-"} - ${member.email ?? "-"}`;

        // 클릭하면 상세 정보 표시
        button.addEventListener("click", function () {
            renderMemberDetail(member);
        });

        // 화면에 회원 버튼 추가
        memberList.append(button);
    });
}


/* ==================================
   7. GET 회원 목록 조회
================================== */

async function loadMembers() {
    // 요청 시작 전 Loading 표시
    renderLoading();

    try {
        // API 서버에 GET 요청
        const response = await fetch(API_URL);

        // 요청 성공 여부 확인
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        // JSON 응답을 JavaScript 데이터로 변환
        members = await response.json();

        // 회원 목록 화면에 출력
        renderMembers();

    } catch (error) {
        // Console 오류 출력
        console.error(error);

        // 화면에 오류 메시지 표시
        renderError("회원 정보를 불러오지 못했습니다.");
    }
}


/* ==================================
   8. 페이지 실행 시 회원 목록 불러오기
================================== */

loadMembers();


/* ==================================
   9. POST 회원 등록 요청 함수
================================== */

async function createMember(member) {
    // 1. 서버에 POST 요청 보내기
    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(member)
    });

    // 2. 요청 성공 여부 확인
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
    }

    // 3. 서버 응답을 JSON으로 변환하여 반환
    return await response.json();
}


/* ==================================
   10. 회원 등록 Form submit 이벤트
================================== */

memberForm.addEventListener("submit", async function (event) {
    // 1. Form 기본 새로고침 방지
    event.preventDefault();

    // 2. Form 입력값 가져오기
    const formData = new FormData(memberForm);

    // 3. 회원 객체 생성
    const inputMember = {
        name: formData.get("name").trim(),
        email: formData.get("email").trim()
    };

    // 4. 빈 값 검사
    if (inputMember.name === "" || inputMember.email === "") {
        formMessage.textContent = "이름과 이메일을 입력하세요.";
        return;
    }

    // 5. 요청 중 메시지 표시
    formMessage.textContent = "등록 요청 중...";

    try {
        // 6. POST 요청 실행
        const createdMember = await createMember(inputMember);

        // 7. 성공 메시지 표시
        formMessage.textContent = "등록 요청 성공";

        // 8. 서버 응답 Console 출력
        console.log("POST Response:", createdMember);

        // 9. 입력창 초기화
        memberForm.reset();

    } catch (error) {
        // 10. 오류 발생 시 처리
        console.error(error);
        formMessage.textContent = "등록 요청 실패";
    }
});