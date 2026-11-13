
import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests",

  // 주문 E2E 테스트 파일만 실행
  testMatch: "store-order-e2e.spec.ts",

  fullyParallel: false,
  workers: 1,
  reporter: "list",

  use: {
    baseURL: "http://localhost:3002",
    browserName: "chromium",
    channel: "msedge",
    headless: true,
  },
});
