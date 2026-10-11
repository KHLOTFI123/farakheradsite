import { Link } from "react-router-dom";
import { useI18n } from "../i18n";
import type { SiteSettings } from "../types";
import { IconArrow, NamedIcon } from "./Icons";

export default function WhySection({ settings }: { settings: SiteSettings }) {
  const { t, to } = useI18n();
  return (
    <section className="container why">
      <div className="why-cta">
        <span>{settings.items.cta_kicker || t("why.fallbackKicker")}</span>
        <h3>{settings.items.cta_title || t("why.fallbackTitle")}</h3>
        <p>{settings.items.cta_text}</p>
        <Link to={to("/contact")} className="btn btn-gold">
          {t("why.cta")}
          <IconArrow />
        </Link>
      </div>
      <div className="stats">
        {settings.stats.map((stat) => (
          <article key={stat.id} className="stat-card">
            <div className="icon-wrap">
              <NamedIcon name={stat.icon} />
            </div>
            <h4>{stat.title}</h4>
            <p className="muted">{stat.description}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
