
"use client";

import { useEffect, useRef, useState } from "react";

import ProductCard from "../../components/mini-popup-store/ProductCard";
import { getProducts } from "../../lib/products-api";
import { createOrder } from "../../lib/orders-api";

import type { Product } from "../../types/product";
import type { CartItem } from "../../types/cart";
import type { OrderResponse } from "../../types/order";

export default function MiniPopupStorePage() {
  // STEP 25: 실제 API 상품 목록
  const [products, setProducts] = useState<Product[]>([]);

  // STEP 21: 장바구니
  const [cart, setCart] = useState<CartItem[]>([]);

  // STEP 26: 상품 조회 상태
  const [isLoading, setIsLoading] = useState(true);
  const [loadError, setLoadError] = useState<string | null>(
    null
  );
  const [retryKey, setRetryKey] = useState(0);

  // STEP 29: 주문 처리 상태
  const [isOrdering, setIsOrdering] = useState(false);
  const [orderError, setOrderError] = useState<string | null>(
    null
  );
  const [orderSuccess, setOrderSuccess] =
    useState<OrderResponse | null>(null);

  // 주문 버튼 연속 클릭으로 중복 요청되는 것 방지
  const orderSubmittingRef = useRef(false);

  // STEP 25~26: 상품 조회 및 다시 시도
  useEffect(() => {
    const controller = new AbortController();

    getProducts(controller.signal)
      .then((data) => {
        if (controller.signal.aborted) return;

        setProducts(data);
        setLoadError(null);
      })
      .catch((error: unknown) => {
        if (controller.signal.aborted) return;

        console.error("상품 조회 오류:", error);
        setLoadError("상품을 불러오지 못했습니다.");
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      });

    return () => {
      controller.abort();
    };
  }, [retryKey]);

  // STEP 26: 상품 재조회
  function handleRetry() {
    setIsLoading(true);
    setLoadError(null);
    setRetryKey((previous) => previous + 1);
  }

  // STEP 21: 상품 장바구니 담기
  function handleAdd(product: Product) {
    if (orderSubmittingRef.current) return;
    if (product.stock <= 0) return;

    setOrderSuccess(null);
    setOrderError(null);

    setCart((previousCart) => {
      const existingItem = previousCart.find(
        (item) => item.id === product.id
      );

      if (existingItem) {
        if (existingItem.quantity >= product.stock) {
          return previousCart;
        }

        return previousCart.map((item) =>
          item.id === product.id
            ? {
                ...item,
                quantity: item.quantity + 1,
              }
            : item
        );
      }

      return [
        ...previousCart,
        { ...product, quantity: 1 },
      ];
    });
  }

  // STEP 22: 장바구니 수량 증가
  function increaseQuantity(productId: number) {
    if (orderSubmittingRef.current) return;

    setOrderError(null);

    setCart((previousCart) =>
      previousCart.map((item) => {
        if (item.id !== productId) return item;

        if (item.quantity >= item.stock) {
          return item;
        }

        return {
          ...item,
          quantity: item.quantity + 1,
        };
      })
    );
  }

  // STEP 22: 장바구니 수량 감소 및 제거
  function decreaseQuantity(productId: number) {
    if (orderSubmittingRef.current) return;

    setOrderError(null);

    setCart((previousCart) =>
      previousCart.flatMap((item) => {
        if (item.id !== productId) {
          return [item];
        }

        if (item.quantity <= 1) {
          return [];
        }

        return [
          {
            ...item,
            quantity: item.quantity - 1,
          },
        ];
      })
    );
  }

  // STEP 23: 총수량 자동 계산
  const totalCount = cart.reduce(
    (sum, item) => sum + item.quantity,
    0
  );

  // STEP 23: 총금액 자동 계산
  const totalPrice = cart.reduce(
    (sum, item) => sum + item.price * item.quantity,
    0
  );

  // STEP 29: 실제 주문 전송
  async function handleSubmitOrder() {
    if (orderSubmittingRef.current || cart.length === 0) {
      return;
    }

    // 중복 클릭 방지
    orderSubmittingRef.current = true;

    setIsOrdering(true);
    setOrderError(null);
    setOrderSuccess(null);

    try {
      // POST /orders
      const result = await createOrder(cart);

      // 주문 성공 결과 표시
      setOrderSuccess(result);

      // 성공한 경우에만 장바구니 초기화
      setCart([]);

      // 주문으로 변경된 실제 재고 다시 불러오기
      setIsLoading(true);
      setLoadError(null);
      setRetryKey((previous) => previous + 1);
    } catch (error: unknown) {
      console.error("주문 처리 오류:", error);

      // 주문 실패 시 장바구니는 그대로 유지
      if (error instanceof Error) {
        setOrderError(error.message);
      } else {
        setOrderError(
          "주문 처리 중 알 수 없는 오류가 발생했습니다."
        );
      }
    } finally {
      orderSubmittingRef.current = false;
      setIsOrdering(false);
    }
  }

  return (
    <main
      style={{
        maxWidth: "1100px",
        margin: "0 auto",
        padding: "32px 20px",
      }}
    >
      <h1>DAY6 미니 팝업스토어</h1>

      <p style={{ margin: "16px 0 24px" }}>
        DAY6 공식 굿즈를 만나보세요 💚
      </p>

      {/* 장바구니 Badge */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          marginBottom: "24px",
          fontWeight: "bold",
        }}
      >
        <span>🛒 장바구니</span>

        <span
          data-testid="cart-count"
          style={{
            backgroundColor: "#171717",
            color: "#ffffff",
            padding: "5px 12px",
            borderRadius: "20px",
          }}
        >
          {totalCount}
        </span>
      </div>

      {/* STEP 26: 상품 조회 상태별 UI */}
      {isLoading ? (
        <p role="status">상품을 불러오는 중...</p>
      ) : loadError ? (
        <div role="alert">
          <p>{loadError}</p>

          <button
            type="button"
            onClick={handleRetry}
            style={{
              marginTop: "12px",
              padding: "10px 20px",
              borderRadius: "8px",
              border: "none",
              backgroundColor: "#171717",
              color: "#ffffff",
              cursor: "pointer",
            }}
          >
            다시 시도
          </button>
        </div>
      ) : products.length === 0 ? (
        <p>등록된 상품이 없습니다.</p>
      ) : (
        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit, minmax(min(100%, 250px), 1fr))",
            gap: "20px",
          }}
        >
          {products.map((product) => (
            <ProductCard
              key={product.id}
              product={product}
              onAdd={handleAdd}
            />
          ))}
        </div>
      )}

      {/* 기존 장바구니 목록 */}
      <section style={{ marginTop: "32px" }}>
        <h2>장바구니 목록</h2>

        {cart.length === 0 ? (
          <p>아직 담은 상품이 없습니다.</p>
        ) : (
          <ul
            style={{
              listStyle: "none",
              padding: 0,
              display: "grid",
              gap: "12px",
            }}
          >
            {cart.map((item) => (
              <li
                key={item.id}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  flexWrap: "wrap",
                  gap: "12px",
                  padding: "14px",
                  border: "1px solid #dddddd",
                  borderRadius: "8px",
                }}
              >
                <div>
                  <strong>
                    {item.name} — {item.quantity}개
                  </strong>

                  <p style={{ margin: "6px 0" }}>
                    {item.price.toLocaleString("ko-KR")}원
                    {" × "}
                    {item.quantity}개
                  </p>

                  <p style={{ margin: 0 }}>
                    소계:{" "}
                    {(
                      item.price * item.quantity
                    ).toLocaleString("ko-KR")}
                    원
                  </p>
                </div>

                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "12px",
                  }}
                >
                  <button
                    type="button"
                    aria-label={`수량 감소: ${item.name}`}
                    onClick={() =>
                      decreaseQuantity(item.id)
                    }
                    disabled={isOrdering}
                  >
                    -
                  </button>

                  <strong>{item.quantity}</strong>

                  <button
                    type="button"
                    aria-label={`수량 증가: ${item.name}`}
                    onClick={() =>
                      increaseQuantity(item.id)
                    }
                    disabled={
                      isOrdering ||
                      item.quantity >= item.stock
                    }
                  >
                    +
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </section>

      {/* STEP 23: 장바구니 합계 */}
      <section
        style={{
          marginTop: "24px",
          padding: "20px",
          backgroundColor: "#f5f5f5",
          borderRadius: "12px",
          color: "#171717",
        }}
      >
        <h2>장바구니 합계</h2>

        <p>
          총수량:{" "}
          <strong data-testid="total-count">
            {totalCount}개
          </strong>
        </p>

        <p>
          총금액:{" "}
          <strong data-testid="total-price">
            {totalPrice.toLocaleString("ko-KR")}원
          </strong>
        </p>

        {/* STEP 29: 실제 주문 버튼 */}
        <button
          type="button"
          data-testid="order-submit"
          onClick={handleSubmitOrder}
          disabled={cart.length === 0 || isOrdering}
          style={{
            width: "100%",
            marginTop: "12px",
            padding: "14px 20px",
            border: "none",
            borderRadius: "8px",
            backgroundColor:
              cart.length === 0 || isOrdering
                ? "#bfbfbf"
                : "#171717",
            color: "#ffffff",
            fontWeight: "bold",
            cursor:
              cart.length === 0 || isOrdering
                ? "not-allowed"
                : "pointer",
          }}
        >
          {isOrdering ? "주문 처리 중..." : "주문하기"}
        </button>

        {/* 주문 실패: 장바구니 보존 */}
        {orderError && (
          <p
            role="alert"
            data-testid="order-error"
            style={{
              marginTop: "16px",
              color: "#b42318",
            }}
          >
            주문 실패: {orderError}
          </p>
        )}

        {/* 주문 성공: 주문 번호 및 서버 계산 금액 */}
        {orderSuccess && (
          <div
            role="status"
            data-testid="order-success"
            style={{
              marginTop: "16px",
              padding: "16px",
              borderRadius: "8px",
              backgroundColor: "#e8f5e9",
              color: "#1b5e20",
            }}
          >
            <strong>주문이 완료되었습니다! 💚</strong>

            <p>
              주문 번호: {orderSuccess.id}
            </p>

            <p>
              주문 금액:{" "}
              {orderSuccess.total_price.toLocaleString(
                "ko-KR"
              )}
              원
            </p>

            <p>
              주문 상태: {orderSuccess.status}
            </p>
          </div>
        )}
      </section>
    </main>
  );
}
