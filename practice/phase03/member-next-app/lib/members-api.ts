
import type { Member } from "../types/member";

// 실제 FastAPI 회원 API 경로
const MEMBERS_PATH = "/members";

// 등록과 수정에 필요한 데이터 타입
export type MemberPayload = Pick<
  Member,
  "name" | "email" | "age"
>;

// API 전체 주소 만들기
function apiUrl(path: string): string {
  const base = process.env.NEXT_PUBLIC_API_BASE_URL;

  if (!base) {
    throw new Error(
      "NEXT_PUBLIC_API_BASE_URL을 설정해 주세요."
    );
  }

  return base.replace(/\/$/, "") + path;
}

// 서버에서 받은 데이터가 Member 타입인지 확인
function isMember(value: unknown): value is Member {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const item = value as Record<string, unknown>;

  return (
    typeof item.member_id === "number" &&
    typeof item.name === "string" &&
    typeof item.email === "string" &&
    typeof item.age === "number"
  );
}

// HTTP 요청 성공 여부 확인
async function requireOk(response: Response): Promise<void> {
  if (!response.ok) {
    throw new Error(
      "회원 API 요청 실패: HTTP " + response.status
    );
  }
}

// READ: 회원 목록 조회
export async function getMembers(
  signal?: AbortSignal
): Promise<Member[]> {
  const response = await fetch(apiUrl(MEMBERS_PATH), {
    cache: "no-store",
    signal,
  });

  await requireOk(response);

  const data: unknown = await response.json();

  if (!Array.isArray(data) || !data.every(isMember)) {
    throw new Error(
      "회원 목록 응답이 예상한 Member[] 형태가 아닙니다."
    );
  }

  return data;
}

// CREATE: 회원 등록
export async function createMember(
  body: MemberPayload
): Promise<void> {
  const response = await fetch(apiUrl(MEMBERS_PATH), {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  await requireOk(response);
}

// UPDATE: 회원 수정
export async function updateMember(
  memberId: number,
  body: MemberPayload
): Promise<void> {
  const response = await fetch(
    apiUrl(MEMBERS_PATH + "/" + memberId),
    {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    }
  );

  await requireOk(response);
}

// DELETE: 회원 삭제
export async function deleteMember(
  memberId: number
): Promise<void> {
  const response = await fetch(
    apiUrl(MEMBERS_PATH + "/" + memberId),
    {
      method: "DELETE",
    }
  );

  // 204 No Content도 성공으로 처리
  await requireOk(response);
}
