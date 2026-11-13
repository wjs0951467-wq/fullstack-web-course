
import type { Product } from "../types/product";

// API 응답의 상품 데이터 형식 확인
function isProduct(value: unknown): value is Product {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const item = value as Record<string, unknown>;

  return (
    typeof item.id === "number" &&
    Number.isInteger(item.id) &&
    typeof item.name === "string" &&
    typeof item.price === "number" &&
    Number.isInteger(item.price) &&
    item.price >= 0 &&
    typeof item.category === "string" &&
    typeof item.stock === "number" &&
    Number.isInteger(item.stock) &&
    item.stock >= 0
  );
}

// PostgreSQL과 연결된 FastAPI 상품 API 호출
export async function getProducts(
  signal?: AbortSignal
): Promise<Product[]> {
  const baseUrl = (
    process.env.NEXT_PUBLIC_API_BASE_URL ||
    "http://127.0.0.1:8001"
  ).replace(/\/+$/, "");

  const response = await fetch(`${baseUrl}/products`, {
    method: "GET",
    cache: "no-store",
    signal,
  });

  if (!response.ok) {
    throw new Error(
      `상품 조회 실패: HTTP ${response.status}`
    );
  }

  const data: unknown = await response.json();

  if (!Array.isArray(data) || !data.every(isProduct)) {
    throw new Error("상품 데이터 형식이 올바르지 않습니다.");
  }

  return data;
}
