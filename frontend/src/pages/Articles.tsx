import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, mediaUrl } from "../api";
import { IconArrow } from "../components/Icons";
import { useI18n } from "../i18n";
import type { Article } from "../types";

export default function Articles() {
  const { lang, t, to } = useI18n();
  const [articles, setArticles] = useState<Article[]>([]);

  useEffect(() => {
    api<Article[]>("/api/articles").then(setArticles).catch(() => setArticles([]));
  }, [lang]);

  return (
    <section className="section">
      <div className="container">
        <div className="page-hero">
          <h1>{t("articles.title")}</h1>
          <p className="muted">{t("articles.lead")}</p>
        </div>
        <div className="article-grid">
          {articles.map((article) => (
            <article key={article.id} className="article-card">
              <img src={mediaUrl(article.image_url)} alt={article.title} />
              <div className="body">
                <h3>{article.title}</h3>
                <p>{article.excerpt}</p>
                <Link to={to(`/articles/${article.slug}`)} className="link-more">
                  {t("articles.more")}
                  <IconArrow />
                </Link>
              </div>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
