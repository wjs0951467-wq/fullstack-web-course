
import { test, expect } from "@playwright/test";

const API_BASE = "http://127.0.0.1:8002";

test("STEP 29 - 실제 주문 생성 E2E", async ({
  page,
  request,
}) => {
  // 1. 테스트 전용 서버인지 먼저 확인
  const healthResponse = await request.get(
    `${API_BASE}/__e2e__/health`
  );

  expect(healthResponse.status()).toBe(200);

  const health = await healthResponse.json();

  expect(health.mode).toBe("isolated-sqlite");
  expect(health.database).toBe("memory");

  // 2. 테스트 전용 DB 초기화
  const resetResponse = await request.post(
    `${API_BASE}/__e2e__/reset`
  );

  expect(resetResponse.status()).toBe(200);

  try {
    // 3. 테스트용 쇼핑몰 접속
    await page.goto("/mini-popup-store");

    // TEST 상품 2개 로딩 확인
    await expect(
      page.locator("article")
    ).toHaveCount(2);

    // 테스트 상품 카드 찾기
    const photoCard = page.locator("article").filter({
      hasText: "TEST DAY6 포토카드",
    });

    const albumCard = page.locator("article").filter({
      hasText: "TEST DAY6 앨범",
    });

    // 4. 초기 재고 확인
    await expect(
      photoCard.getByText("재고 10개")
    ).toBeVisible();

    await expect(
      albumCard.getByText("재고 5개")
    ).toBeVisible();

    // 5. 포토카드 2개 장바구니에 담기
    await photoCard
      .getByRole("button", {
        name: "장바구니 담기",
      })
      .click();

    await photoCard
      .getByRole("button", {
        name: "장바구니 담기",
      })
      .click();

    // 6. 앨범 1개 장바구니에 담기
    await albumCard
      .getByRole("button", {
        name: "장바구니 담기",
      })
      .click();

    // 총수량 3개, 총금액 30,000원
    await expect(
      page.getByTestId("cart-count")
    ).toHaveText("3");

    await expect(
      page.getByTestId("total-price")
    ).toContainText("30,000원");

    // 7. 실제 POST /orders 요청 감시
    const orderResponsePromise = page.waitForResponse(
      (response) =>
        response.url() === `${API_BASE}/orders` &&
        response.request().method() === "POST"
    );

    // 주문하기 클릭
    await page.getByTestId("order-submit").click();

    // 8. 실제 서버 응답 확인
    const orderResponse = await orderResponsePromise;

    expect(orderResponse.status()).toBe(201);

    const orderData = await orderResponse.json();

    expect(orderData).toEqual(
      expect.objectContaining({
        total_price: 30000,
        status: "created",
        items: expect.arrayContaining([
          expect.objectContaining({
            product_id: 101,
            quantity: 2,
            price: 5000,
          }),
          expect.objectContaining({
            product_id: 102,
            quantity: 1,
            price: 20000,
          }),
        ]),
      })
    );

    expect(orderData.id).toBeGreaterThan(0);
    expect(orderData.items).toHaveLength(2);

    // 9. 주문 완료 메시지 확인
    const successMessage = page.getByTestId(
      "order-success"
    );

    await expect(successMessage).toBeVisible();

    await expect(successMessage).toContainText(
      "주문이 완료되었습니다!"
    );

    await expect(successMessage).toContainText(
      "30,000원"
    );

    // 10. 주문 성공 후 장바구니 초기화 확인
    await expect(
      page.getByTestId("cart-count")
    ).toHaveText("0");

    await expect(
      page.getByTestId("total-price")
    ).toContainText("0원");

    await expect(
      page.getByTestId("order-submit")
    ).toBeDisabled();

    // 11. 상품 재조회 후 감소한 재고 확인
    await expect(
      photoCard.getByText("재고 8개")
    ).toBeVisible();

    await expect(
      albumCard.getByText("재고 4개")
    ).toBeVisible();

    // 12. 테스트 DB의 재고도 직접 확인
    const productsResponse = await request.get(
      `${API_BASE}/products`
    );

    expect(productsResponse.status()).toBe(200);

    const products = await productsResponse.json();

    expect(products).toEqual(
      expect.arrayContaining([
        expect.objectContaining({
          id: 101,
          stock: 8,
        }),
        expect.objectContaining({
          id: 102,
          stock: 4,
        }),
      ])
    );
  } finally {
    // 테스트 성공·실패와 관계없이
    // 테스트 전용 SQLite 데이터 초기화
    await request.post(`${API_BASE}/__e2e__/reset`);
  }
});
