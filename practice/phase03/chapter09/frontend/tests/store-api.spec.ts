
import { test, expect } from "@playwright/test";

test("STEP 25 - 실제 FastAPI 상품 조회", async ({ page }) => {
  // 실제 FastAPI의 GET /products 성공 응답 기다리기
  const responsePromise = page.waitForResponse(
    (response) =>
      response.url() === "http://127.0.0.1:8001/products" &&
      response.request().method() === "GET" &&
      response.status() === 200
  );

  // DAY6 미니 팝업스토어 접속
  await page.goto("/mini-popup-store");

  // 실제 API 응답 확인
  const response = await responsePromise;

  expect(response.status()).toBe(200);

  const data: unknown = await response.json();

  // 상품 응답이 배열인지 확인
  expect(Array.isArray(data)).toBe(true);

  if (!Array.isArray(data)) {
    throw new Error("상품 API 응답이 배열이 아닙니다.");
  }

  // 실제 상품 6개 조회 확인
  expect(data).toHaveLength(6);

  // 실제 앨범 상품 찾기
  const album = data.find(
    (item) =>
      typeof item === "object" &&
      item !== null &&
      item.id === 4
  );

  // 변하지 않아야 하는 상품 정보 검사
  expect(album).toEqual(
    expect.objectContaining({
      id: 4,
      name: "DAY6 정규 4집 The DECADE",
      price: 19300,
      category: "Album",
    })
  );

  // 재고는 주문에 따라 달라지므로
  // 12개 같은 고정 수량 대신 유효한 값인지 검사
  expect(Number.isInteger(album?.stock)).toBe(true);
  expect(album.stock).toBeGreaterThanOrEqual(0);

  // React 상품 카드 6개 표시 확인
  await expect(page.locator("article")).toHaveCount(6);

  // 앨범 상품명과 가격 확인
  const albumCard = page.locator("article").filter({
    hasText: "DAY6 정규 4집 The DECADE",
  });

  await expect(albumCard).toBeVisible();

  await expect(
    albumCard.getByText("19,300원")
  ).toBeVisible();

  // 품절 상품 버튼 확인
  const soldOutCard = page.locator("article").filter({
    hasText: "FOREVER YOUNG 월드투어 Blu-ray",
  });

  await expect(
    soldOutCard.getByRole("button", { name: "품절" })
  ).toBeDisabled();
});
