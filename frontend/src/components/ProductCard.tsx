import { Link } from "react-router-dom";
import { mediaUrl } from "../api";
import { useI18n } from "../i18n";
import type { Product } from "../types";
import { IconArrow } from "./Icons";

export default function ProductCard({
  product,
  promo = false,
}: {
  product: Product;
  promo?: boolean;
}) {
  const { t, to } = useI18n();
  return (
    <article className="product-card">
      <div className="card-media">
        <img src={mediaUrl(product.image_url)} alt={product.title} />
        {promo ? <span className="price-promo">Prices – Limited Time Only</span> : null}
      </div>
      <div className="body">
        <h3>{product.title}</h3>
        <p>{product.summary}</p>
        <Link to={to(`/products/${product.slug}`)} className="link-more">
          {t("product.details")}
          <IconArrow />
        </Link>
      </div>
    </article>
  );
}
