import { useEffect, useMemo, useState } from "react";
import { Link, useSearchParams } from "react-router-dom";
import { api } from "../api";
import { useI18n } from "../i18n";
import type { Article, Product } from "../types";

export default function Search() {
  const [params] = useSearchParams();
  const q = (params.get("q") || "").trim();
  const { lang, t, to } = useI18n();
  const [products, setProducts] = useState<Product[]>([]);
  const [articles, setArticles] = useState<Article[]>([]);

  useEffect(() => {
    Promise.all([api<Product[]>("/api/products"), api<Article[]>("/api/articles")])
      .then(([p, a]) => {
        setProducts(p);
        setArticles(a);
      })
      .catch(() => undefined);
  }, [lang]);

  const productHits = useMemo(
    () => products.filter((item) => `${item.title} ${item.summary} ${item.description}`.toLowerCase().includes(q.toLowerCase())),
    [products, q],
  );
  const articleHits = useMemo(
    () => articles.filter((item) => `${item.title} ${item.excerpt} ${item.content}`.toLowerCase().includes(q.toLowerCase())),
    [articles, q],
  );

  return (
    <section className="section">
      <div className="container">
        <div className="page-hero">
          <h1>{t("search.title")}</h1>
          <p className="muted">{t("search.query")}: {q || "—"}</p>
        </div>
        <h3>{t("search.products")}</h3>
        {productHits.length === 0 && <p className="muted">{t("search.noProducts")}</p>}
        {productHits.map((item) => (
          <p key={item.id}><Link to={to(`/products/${item.slug}`)}>{item.title}</Link></p>
        ))}
        <h3>{t("search.articles")}</h3>
        {articleHits.length === 0 && <p className="muted">{t("search.noArticles")}</p>}
        {articleHits.map((item) => (
          <p key={item.id}><Link to={to(`/articles/${item.slug}`)}>{item.title}</Link></p>
        ))}
      </div>
    </section>
  );
}
