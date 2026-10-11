import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api, mediaUrl } from "../api";
import { useI18n } from "../i18n";
import type { Article } from "../types";
import NotFound from "./NotFound";

export default function ArticleDetail() {
  const { slug } = useParams();
  const { lang, t } = useI18n();
  const [article, setArticle] = useState<Article | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!slug) return;
    setArticle(null);
    setError("");
    api<Article>(`/api/articles/${slug}`).then(setArticle).catch((err: Error) => setError(err.message));
  }, [slug, lang]);

  if (error) return <NotFound />;
  if (!article) return <div className="container section"><p className="muted">{t("common.loading")}</p></div>;

  return (
    <section className="section">
      <div className="container article-detail">
        <img src={mediaUrl(article.image_url)} alt={article.title} />
        <h1>{article.title}</h1>
        <p className="muted">{article.excerpt}</p>
        {article.content.split("\n\n").map((paragraph) => (
          <p key={paragraph.slice(0, 32)}>{paragraph}</p>
        ))}
      </div>
    </section>
  );
}