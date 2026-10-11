import { useEffect, useMemo, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { api, mediaUrl } from "../api";
import { useI18n } from "../i18n";
import { IconArrow } from "../components/Icons";
import { parseServiceDetails } from "../serviceUtils";
import type { ServiceItem } from "../types";
import NotFound from "./NotFound";

export default function ServiceDetail() {
  const { slug } = useParams();
  const { lang, t, to } = useI18n();
  const [service, setService] = useState<ServiceItem | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!slug) return;
    setService(null);
    setError("");
    api<ServiceItem>(`/api/services/${slug}`)
      .then(setService)
      .catch((err: Error) => setError(err.message));
  }, [slug, lang]);

  const details = useMemo(() => parseServiceDetails(service?.details), [service]);

  if (error) {
    return <NotFound />;
  }
  if (!service) {
    return <div className="container section"><p className="muted">{t("common.loading")}</p></div>;
  }

  const image = service.image_url || "";

  return (
    <section className="section">
      <div className="container">
        <nav className="crumb" aria-label={t("service.nav")}>
          <Link to={to("/")}>{t("service.home")}</Link>
          <span>‹</span>
          <Link to={to("/services")}>{t("nav.services")}</Link>
          <span>‹</span>
          <span>{service.title}</span>
        </nav>

        <div className="detail service-detail-hero">
          <div>
            {details.kicker && <p className="service-kicker">{details.kicker}</p>}
            <h1>{service.title}</h1>
            <p className="muted">{details.lead || service.description}</p>
            <div className="hero-actions">
              <Link to={to("/contact")} className="btn btn-gold">
                {t("service.start")}
                <IconArrow />
              </Link>
              <Link to={to("/contact")} className="btn btn-outline">{t("service.contact")}</Link>
            </div>
          </div>
          {image ? <img src={mediaUrl(image)} alt={service.title} /> : null}
        </div>

        {!!details.intro?.length && (
          <div className="service-intro">
            {details.intro_title && <h2>{details.intro_title}</h2>}
            {details.intro.map((paragraph) => (
              <p key={paragraph.slice(0, 40)}>{paragraph}</p>
            ))}
          </div>
        )}

        {!!details.offerings?.length && (
          <div className="product-block">
            <div className="section-head">
              <div>
                <h2>{details.offerings_title || t("service.offerings")}</h2>
                {details.offerings_lead && <p>{details.offerings_lead}</p>}
              </div>
            </div>
            <div className="offerings-grid">
              {details.offerings.map((item) => (
                <article key={item.title} className="content-card offering-card">
                  <h3>{item.title}</h3>
                </article>
              ))}
            </div>
          </div>
        )}

        {!!details.why?.length && (
          <div className="product-block">
            <div className="section-head">
              <div>
                <h2>{details.why_title || t("why.fallbackKicker")}</h2>
                {details.why_lead && <p>{details.why_lead}</p>}
              </div>
            </div>
            <div className="service-why-grid">
              {details.why.map((item) => (
                <article key={item.title} className="content-card product-point">
                  <h3>{item.title}</h3>
                  <p>{item.text}</p>
                </article>
              ))}
            </div>
          </div>
        )}

        {(details.cta_lead || details.cta_text) && (
          <div className="service-cta-band">
            {details.cta_lead && <p>{details.cta_lead}</p>}
            {details.cta_text && <h2>{details.cta_text}</h2>}
            <div className="hero-actions">
              <Link to={to("/contact")} className="btn btn-gold">
                {t("service.start")}
                <IconArrow />
              </Link>
              <Link to={to("/contact")} className="btn btn-outline">{t("service.contact")}</Link>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
