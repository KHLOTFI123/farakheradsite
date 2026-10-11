import { useI18n } from "../i18n";
import { useSite } from "../siteContext";

export default function About() {
  const { items } = useSite();
  const { t } = useI18n();

  return (
    <section className="section">
      <div className="container">
        <div className="page-hero">
          <h1>{items.about_title || t("about.fallback")}</h1>
          <p className="muted">{items.tagline}</p>
        </div>
        <div className="content-card" style={{ padding: 28, maxWidth: 820 }}>
          <p>{items.about_text}</p>
        </div>
      </div>
    </section>
  );
}
