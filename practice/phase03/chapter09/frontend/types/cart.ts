
import type { Product } from "./product";

// Product의 모든 정보 + 장바구니 수량
export type CartItem = Product & {
  quantity: number;
};
