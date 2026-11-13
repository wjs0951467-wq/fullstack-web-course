
"use client";

import type { Product } from "../../types/product";
import styles from "./ProductCard.module.css";

type ProductCardProps = {
  product: Product;
  onAdd: (product: Product) => void;
};

export default function ProductCard({
  product,
  onAdd,
}: ProductCardProps) {
  const soldOut = product.stock === 0;

  return (
    <article className={styles.card}>
      <p className={styles.category}>
        {product.category}
      </p>

      <h2 className={styles.name}>
        {product.name}
      </h2>

      <p className={styles.price}>
        {product.price.toLocaleString("ko-KR")}원
      </p>

      <p className={styles.stock}>
        {soldOut ? "품절" : `재고 ${product.stock}개`}
      </p>

      <button
        type="button"
        className={styles.button}
        disabled={soldOut}
        onClick={() => onAdd(product)}
      >
        {soldOut ? "품절" : "장바구니 담기"}
      </button>
    </article>
  );
}
