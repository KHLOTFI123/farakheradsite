import { Link } from "react-router-dom";
import { useI18n } from "../i18n";
import { useSite } from "../siteContext";
import { IconInstagram, IconLinkedin, LogoMark } from "./Icons";

export default function Footer() {
  const { items } = useSite();
  const { t, to, lang } = useI18n();
  const name = items.company_name || "فرا خرد";
  const year = lang === "fa" || lang === "fa-AF" ? "۱۴۰۵" : "2026";

  return (
    <footer className="site-footer">
      <div className="container footer-grid">
        <div>
          <Link to={to("/")} className="brand" aria-label={name}>
            <LogoMark />
          </Link>
          <p>{items.footer_text || t("footer.fallback")}</p>
          <div className="socials">
            <a href="https://instagram.com" target="_blank" rel="noreferrer" aria-label={t("footer.instagram")}>
              <IconInstagram />
            </a>
            <a href={items.linkedin || "https://linkedin.com"} target="_blank" rel="noreferrer" aria-label={t("footer.linkedin")}>
              <IconLinkedin />
            </a>
          </div>
        </div>
        <div>
          <h4>{t("footer.quick")}</h4>
          <Link to={to("/about")}>{t("nav.about")}</Link>
          <Link to={to("/contact")}>{t("nav.contact")}</Link>
          <Link to={to("/products")}>{t("nav.products")}</Link>
        </div>
        <div>
          <h4>{t("footer.services")}</h4>
          <Link to={to("/services/devops")}>{t("footer.devops")}</Link>
          <Link to={to("/services/mlops")}>{t("footer.mlops")}</Link>
          <Link to={to("/articles")}>{t("nav.articles")}</Link>
        </div>
        <div>
          <h4>{t("footer.contact")}</h4>
          <p>{items.phone || "02177132703"}</p>
          <p>{items.mobile || "09121788139"}</p>
          <p>{items.address || "تهران، ایران"}</p>
        </div>
      </div>
      <div className="container copy">© {year} {name}. {t("footer.rights")}</div>
    </footer>
  );
}
