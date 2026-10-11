import { useEffect, useState } from "react";
import { api } from "../api";
import ProductCard from "../components/ProductCard";
import { useI18n } from "../i18n";
import type { Product } from "../types";

export default function Products() {
  const { lang, t } = useI18n();
  const [products, setProducts] = useState<Product[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    api<Product[]>("/api/products").then(setProducts).catch((err: Error) => setError(err.message));
  }, [lang]);

  return (
    <section className="section">
      <div className="container">
        <div className="page-hero">
          <h1>{t("products.title")}</h1>
          <p className="muted">{t("products.lead")}</p>
        </div>
        {error && <p className="error">{error}</p>}
        <div className="product-grid">
          {products.map((product) => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </div>
    </section>
  );
}
