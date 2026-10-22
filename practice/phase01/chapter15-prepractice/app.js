const searchForm = document.querySelector("#search-form");
const searchInput = document.querySelector("#search-input");
const statusMessage = document.querySelector("#status-message");
const bookList = document.querySelector("#book-list");
const bookDetail = document.querySelector("#book-detail");
const bookForm = document.querySelector("#book-form");
const formMessage = document.querySelector("#form-message");

const SEARCH_API_URL = "https://openlibrary.org/search.json";
const POST_API_URL = "https://jsonplaceholder.typicode.com/posts";

let books = [];

 // STEP 06 + STEP 11 — 검색 Form submit Event 연결
searchForm.addEventListener("submit", async function (event) {
    // 1. Form의 기본 새로고침 방지
    event.preventDefault();

    // 2. 검색어 읽고 앞뒤 공백 제거
    const keyword = searchInput.value.trim();

    // 3. 검색어가 비어 있으면 종료
    if (keyword === "") {
        statusMessage.textContent = "검색어를 입력하세요.";
        return;
    }

    // 4. 검색 중 상태 표시
    renderLoading();

    // 5. GET 요청 및 검색 결과 출력
    try {
        books = await searchBooks(keyword);
        renderBooks();
    } catch (error) {
        // 6. 오류 발생 시 처리
        console.error(error);
        renderError("도서를 불러오지 못했습니다.");
    }
});

 // STEP 07 — GET 도서 검색 함수
async function searchBooks(keyword) {
    const url = `${SEARCH_API_URL}?q=${encodeURIComponent(keyword)}&limit=10&fields=key,title,author_name,first_publish_year`;

    const response = await fetch(url);

    if (!response.ok) {
        throw new Error("도서 검색 요청에 실패했습니다.");
    }

    const data = await response.json();

    return data.docs;
}

 // STEP 08 — Loading / Error / Empty 상태 처리

// 1. 검색 중일 때
function renderLoading() {
    statusMessage.textContent = "도서를 검색하는 중입니다...";
    bookList.replaceChildren();
    bookDetail.textContent = "도서를 선택하세요.";
}

// 2. 오류가 발생했을 때
function renderError(message) {
    statusMessage.textContent = message;
    bookList.replaceChildren();
    bookDetail.textContent = "도서를 선택하세요.";
}

// 3. 검색 결과가 없을 때
function renderEmpty() {
    statusMessage.textContent = "검색 결과가 없습니다.";
    bookList.replaceChildren();
    bookDetail.textContent = "도서를 선택하세요.";
}


 // STEP 09 — 도서 목록 렌더링
function renderBooks() {
    // 1. 기존 도서 목록 비우기
    bookList.replaceChildren();

    // 2. 검색 결과가 없으면 Empty 상태 표시
    if (books.length === 0) {
        renderEmpty();
        return;
    }

    // 3. 검색 결과 개수 표시
    statusMessage.textContent = `검색 결과 ${books.length}권`;

    // 4. 도서 배열을 순회하며 버튼 생성
    books.forEach(function (book) {
        // 저자 정보 처리
        const authors =
            Array.isArray(book.author_name) && book.author_name.length > 0
                ? book.author_name.join(", ")
                : "저자 정보 없음";

        // 최초 출판연도 처리
        const year = book.first_publish_year ?? "-";

        // 도서 버튼 생성
        const button = document.createElement("button");
        button.type = "button";

        // 도서 정보 표시
        button.textContent = `${book.title ?? "-"} / ${authors} / ${year}`;

        // 5. 버튼 클릭 시 상세 정보 표시
        button.addEventListener("click", function () {
            renderBookDetail(book);
        });

        // 6. 생성한 버튼을 목록에 추가
        bookList.append(button);
    });
}


 // STEP 10 — 도서 상세 보기
function renderBookDetail(book) {
    // 1. 기존 상세 정보 비우기
    bookDetail.replaceChildren();

    // 2. 저자 정보 처리
    const authors =
        Array.isArray(book.author_name) && book.author_name.length > 0
            ? book.author_name.join(", ")
            : "저자 정보 없음";

    // 3. 나머지 데이터 처리
    const title = book.title ?? "-";
    const year = book.first_publish_year ?? "-";
    const key = book.key ?? "-";

    // 4. 상세 정보 항목 만들기
    const details = [
        `제목: ${title}`,
        `저자: ${authors}`,
        `최초 출판연도: ${year}`,
        `Open Library key: ${key}`
    ];

    // 5. 각 항목을 HTML 요소로 생성하여 출력
    details.forEach(function (detail) {
        const p = document.createElement("p");
        p.textContent = detail;
        bookDetail.append(p);
    });
}



 // STEP 13 + STEP 15 — 도서 등록 Form submit Event 연결
bookForm.addEventListener("submit", async function (event) {
    // 1. Form 기본 새로고침 방지
    event.preventDefault();

    // 2. FormData로 입력값 가져오기
    const formData = new FormData(bookForm);

    // 3. 제목과 저자 읽기 (앞뒤 공백 제거)
    const title = formData.get("title").trim();
    const author = formData.get("author").trim();

    // 4. 빈 값 검사
    if (title === "" || author === "") {
        formMessage.textContent = "제목과 저자를 입력하세요.";
        return;
    }

    // 5. 도서 등록 요청 객체 생성
    const bookRequest = {
        title: title,
        author: author
    };

    // 6. 등록 요청 중 메시지 표시
    formMessage.textContent = "등록 요청 중...";

    // 7. POST 요청 실행
    try {
        const responseData = await createBookRequest(bookRequest);

        // 8. 성공 메시지 표시
        formMessage.textContent = "등록 요청이 성공했습니다.";

        // 9. POST 응답 Console 출력
        console.log("POST Response:", responseData);

        // 10. 등록 Form 초기화
        bookForm.reset();

    } catch (error) {
        // 11. 오류 Console 출력
        console.error(error);

        // 12. 실패 메시지 표시
        formMessage.textContent = "등록 요청에 실패했습니다.";
    }
});


 // STEP 14 — POST 도서 등록 요청 함수
async function createBookRequest(book) {
    // 1. POST 요청 보내기
    const response = await fetch(POST_API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(book)
    });

    // 2. 응답 성공 여부 확인
    if (!response.ok) {
        throw new Error("도서 등록 요청에 실패했습니다.");
    }

    // 3. JSON 응답 데이터 변환
    const data = await response.json();

    // 4. 응답 결과 반환
    return data;
}