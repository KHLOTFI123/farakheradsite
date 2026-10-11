import { Link } from "react-router-dom";
import { useI18n } from "../i18n";

export default function NotFound() {
  const { t, to } = useI18n();

  return (
    <section className="section">
      <div className="container page-hero" style={{ maxWidth: 640 }}>
        <p className="muted">404</p>
        <h1>{t("missing.title")}</h1>
        <p className="muted">{t("missing.text")}</p>
        <div className="hero-actions" style={{ marginTop: 20 }}>
          <Link to={to("/")} className="btn btn-gold">{t("missing.home")}</Link>
          <Link to={to("/products")} className="btn btn-outline">{t("missing.products")}</Link>
        </div>
      </div>
    </section>
  );
}
