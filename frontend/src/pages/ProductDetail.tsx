import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, mediaUrl } from "../api";
import { useI18n } from "../i18n";
import type { Product, ProductDetails } from "../types";
import NotFound from "./NotFound";

function parseDetails(raw?: string): ProductDetails {
  try {
    return JSON.parse(raw || "{}") as ProductDetails;
  } catch {
    return {};
  }
}

export default function ProductDetail() {
  const { slug } = useParams();
  const { lang, t, to } = useI18n();
  const [product, setProduct] = useState<Product | null>(null);
  const [catalog, setCatalog] = useState<Product[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!slug) return;
    setProduct(null);
    setError("");
    Promise.all([api<Product>(`/api/products/${slug}`), api<Product[]>("/api/products")])
      .then(([item, list]) => {
        setProduct(item);
        setCatalog(list);
      })
      .catch((err: Error) => setError(err.message));
  }, [slug, lang]);

  const details = useMemo(() => parseDetails(product?.details), [product]);
  const related = useMemo(
    () => catalog.filter((item) => (details.related || []).includes(item.slug)),
    [catalog, details.related],
  );

  if (error) {
    return <NotFound />;
  }
  if (!product) {
    return <div className="container section"><p className="muted">{t("common.loading")}</p></div>;
  }

  return (
    <section className="section">
      <div className="container">
        <div className="detail">
          <img src={mediaUrl(product.image_url)} alt={product.title} />
          <div>
            <h1>{product.title}</h1>
            {details.tagline && <p className="muted">{details.tagline}</p>}
            <p className="muted">{product.summary}</p>
            {product.description.split("\n\n").map((paragraph) => (
              <p key={paragraph.slice(0, 32)}>{paragraph}</p>
            ))}
            <Link to={to("/contact")} className="btn btn-gold">{t("product.demo")}</Link>
          </div>
        </div>

        {!!details.features?.length && (
          <div className="product-block">
            <h2>{t("product.features")}</h2>
            <div className="product-grid">
              {details.features.map((item) => (
                <article key={item.title} className="content-card product-point">
                  <h3>{item.title}</h3>
                  <p>{item.text}</p>
                </article>
              ))}
            </div>
          </div>
        )}

        {!!details.benefits?.length && (
          <div className="product-block">
            <h2>{t("product.benefits")}</h2>
            <div className="product-grid">
              {details.benefits.map((item) => (
                <article key={item.title} className="content-card product-point">
                  <h3>{item.title}</h3>
                  <p>{item.text}</p>
                </article>
              ))}
            </div>
          </div>
        )}

        {!!details.audiences?.length && (
          <div className="product-block">
            <h2>{t("product.audiences")}</h2>
            <ul className="audience-list">
              {details.audiences.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        )}

        {!!details.steps?.length && (
          <div className="product-block">
            <h2>{t("product.steps")}</h2>
            <ol className="step-list">
              {details.steps.map((item, index) => (
                <li key={item.title}>
                  <span>{index + 1}</span>
                  <div>
                    <h3>{item.title}</h3>
                    <p>{item.text}</p>
                  </div>
                </li>
              ))}
            </ol>
          </div>
        )}

        {!!details.faqs?.length && (
          <div className="product-block">
            <h2>{t("product.faqs")}</h2>
            <div className="faq-list">
              {details.faqs.map((item) => (
                <details key={item.q} className="content-card faq-item">
                  <summary>{item.q}</summary>
                  <p>{item.a}</p>
                </details>
              ))}
            </div>
          </div>
        )}

        {!!related.length && (
          <div className="product-block">
            <h2>{t("product.related")}</h2>
            <div className="related-list">
              {related.map((item) => (
                <Link key={item.id} to={to(`/products/${item.slug}`)} className="content-card related-card">
                  <strong>{item.title}</strong>
                  <p className="muted">{item.summary}</p>
                </Link>
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
