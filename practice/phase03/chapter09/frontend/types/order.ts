
export type OrderItemCreate = {
  product_id: number;
  quantity: number;
};

export type OrderCreate = {
  items: OrderItemCreate[];
};

export type OrderItemResponse = {
  product_id: number;
  quantity: number;
  price: number;
};

export type OrderResponse = {
  id: number;
  total_price: number;
  status: string;
  created_at: string;
  items: OrderItemResponse[];
};
