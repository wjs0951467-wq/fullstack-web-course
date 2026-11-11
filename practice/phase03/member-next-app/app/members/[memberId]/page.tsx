
import { Suspense } from "react";
import MemberDetail from "../../../components/MemberDetail";

export default function MemberDetailPage() {
  return (
    <main
      style={{
        maxWidth: 880,
        margin: "48px auto",
        padding: "0 24px",
        fontFamily: "Arial, sans-serif",
      }}
    >
      <Suspense
        fallback={
          <p role="status">
            회원 상세 화면을 준비 중입니다...
          </p>
        }
      >
        <MemberDetail />
      </Suspense>
    </main>
  );
}
