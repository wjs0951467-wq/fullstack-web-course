
import type { CartItem } from "../types/cart";
import type {
  OrderCreate,
  OrderResponse,
} from "../types/order";

// HTTP 오류 코드와 오류 메시지를 함께 보관
export class OrderApiError extends Error {
  constructor(
    public readonly status: number,
    message: string
  ) {
    super(message);
    this.name = "OrderApiError";
  }
}

// FastAPI 주문 응답의 기본 형식 검증
function isOrderResponse(
  value: unknown
): value is OrderResponse {
  if (typeof value !== "object" || value === null) {
    return false;
  }

  const order = value as Record<string, unknown>;

  if (
    typeof order.id !== "number" ||
    typeof order.total_price !== "number" ||
    typeof order.status !== "string" ||
    typeof order.created_at !== "string" ||
    !Array.isArray(order.items)
  ) {
    return false;
  }

  return order.items.every((value: unknown) => {
    if (
      typeof value !== "object" ||
      value === null
    ) {
      return false;
    }

    const item = value as Record<string, unknown>;

    return (
      typeof item.product_id === "number" &&
      typeof item.quantity === "number" &&
      typeof item.price === "number"
    );
  });
}

// HTTP 오류가 발생했을 때 FastAPI의 detail 메시지 확인
async function readErrorMessage(
  response: Response
): Promise<string> {
  const fallback = `주문 실패: HTTP ${response.status}`;

  try {
    const data: unknown = await response.json();

    if (
      typeof data === "object" &&
      data !== null &&
      "detail" in data &&
      typeof data.detail === "string"
    ) {
      return data.detail;
    }
  } catch {
    // JSON 응답이 아니면 기본 오류 메시지 사용
  }

  return fallback;
}

// 장바구니 내용을 실제 주문 API로 전송
export async function createOrder(
  cart: CartItem[]
): Promise<OrderResponse> {
  if (cart.length === 0) {
    throw new Error("장바구니가 비어 있습니다.");
  }

  const baseUrl = (
    process.env.NEXT_PUBLIC_API_BASE_URL ||
    "http://127.0.0.1:8001"
  ).replace(/\/+$/, "");

  // 서버에는 상품 ID와 수량만 전송
  // 가격은 FastAPI가 DB에서 직접 조회해서 계산
  const payload: OrderCreate = {
    items: cart.map((item) => ({
      product_id: item.id,
      quantity: item.quantity,
    })),
  };

  const response = await fetch(`${baseUrl}/orders`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const message = await readErrorMessage(response);

    throw new OrderApiError(
      response.status,
      message
    );
  }

  // 정상 주문은 HTTP 201 Created
  if (response.status !== 201) {
    throw new Error(
      `예상하지 못한 주문 응답: HTTP ${response.status}`
    );
  }

  const data: unknown = await response.json();

  if (!isOrderResponse(data)) {
    throw new Error(
      "주문 API 응답 형식이 올바르지 않습니다."
    );
  }

  return data;
}
