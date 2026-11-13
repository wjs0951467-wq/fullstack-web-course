
import { test, expect } from "@playwright/test";

test("STEP 19 - DAY6 상품 카드 표시", async ({ page }) => {
  const keyWarnings: string[] = [];

  // React key 관련 경고 수집
  page.on("console", (message) => {
    if (
      ["warning", "error"].includes(message.type()) &&
      /unique.*key|same key|encountered two children/i.test(
        message.text()
      )
    ) {
      keyWarnings.push(message.text());
    }
  });

  // DAY6 쇼핑몰 접속
  await page.goto("/mini-popup-store");

  // 페이지 제목 확인
  await expect(
    page.getByRole("heading", {
      name: "DAY6 미니 팝업스토어",
    })
  ).toBeVisible();

  // 상품 카드 6개 확인
  const cards = page.locator("article");
  await expect(cards).toHaveCount(6);

  // 품절 상품 확인
  const soldOutCard = cards.filter({
    hasText: "FOREVER YOUNG 월드투어 Blu-ray",
  });

  await expect(
    soldOutCard.getByRole("button", { name: "품절" })
  ).toBeDisabled();

  // 장바구니 버튼 5개 확인
  await expect(
    page.getByRole("button", {
      name: "장바구니 담기",
    })
  ).toHaveCount(5);

  // React key 경고 없는지 확인
  expect(keyWarnings).toEqual([]);
});
