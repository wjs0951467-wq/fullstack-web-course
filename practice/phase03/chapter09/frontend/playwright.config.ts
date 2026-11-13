
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",

  // 격리 DB 주문 테스트는 별도 설정으로만 실행
  testIgnore: ["**/store-order-e2e.spec.ts"],

  fullyParallel: false,

  reporter: "list",

  use: {
    baseURL: "http://localhost:3001",
    browserName: "chromium",
    channel: "msedge",
    headless: true,
  },
});
