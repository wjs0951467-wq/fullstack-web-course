
import { test, expect } from "@playwright/test";

test("STEP 21 - 장바구니 수량 증가", async ({ page }) => {
  await page.goto("/mini-popup-store");

  const badge = page.getByTestId("cart-count");

  // 초기 장바구니는 0개
  await expect(badge).toHaveText("0");

  const addButtons = page.getByRole("button", {
    name: "장바구니 담기",
  });

  // 첫 번째 상품 담기
  await addButtons.nth(0).click();
  await expect(badge).toHaveText("1");

  // 같은 상품 다시 담기
  await addButtons.nth(0).click();
  await expect(badge).toHaveText("2");

  await expect(
    page.getByText(
      "The DECADE FINALE 트레이딩 카드 — 2개"
    )
  ).toBeVisible();

  // 다른 상품 담기
  await addButtons.nth(1).click();
  await expect(badge).toHaveText("3");

  // 품절 상품 버튼 확인
  await expect(
    page.getByRole("button", { name: "품절" })
  ).toBeDisabled();
});

test("STEP 21 - 재고 상한 초과 방지", async ({ page }) => {
  await page.goto("/mini-popup-store");

  const badge = page.getByTestId("cart-count");

  // 재고 8개인 응원봉 상품
  const fanlightCard = page.locator("article").filter({
    hasText: "DAY6 OFFICIAL LIGHT BAND VER 3",
  });

  const addButton = fanlightCard.getByRole("button", {
    name: "장바구니 담기",
  });

  // 재고만큼 담기
  for (let i = 0; i < 8; i++) {
    await addButton.click();
  }

  await expect(badge).toHaveText("8");

  // 한 번 더 클릭해도 증가하면 안 됨
  await addButton.click();
  await expect(badge).toHaveText("8");
});
