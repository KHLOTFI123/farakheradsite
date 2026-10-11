import { useEffect, useMemo, useState } from "react";
import { api } from "../api";
import ServiceCard from "../components/ServiceCard";
import { useI18n } from "../i18n";
import { isFeaturedService } from "../serviceUtils";
import type { ServiceItem } from "../types";

export default function Services() {
  const { lang, t } = useI18n();
  const [services, setServices] = useState<ServiceItem[]>([]);

  useEffect(() => {
    api<ServiceItem[]>("/api/services").then(setServices).catch(() => setServices([]));
  }, [lang]);

  const featured = useMemo(() => services.filter(isFeaturedService), [services]);
  const extras = useMemo(() => services.filter((item) => !isFeaturedService(item)), [services]);

  return (
    <section className="section">
      <div className="container">
        <div className="page-hero">
          <h1>{t("services.title")}</h1>
          <p className="muted">{t("services.lead")}</p>
        </div>
        <div className="section-head">
          <div>
            <h2>{t("services.domains")}</h2>
            <p>{t("services.domainsLead")}</p>
          </div>
        </div>
        <div className="service-domains">
          {featured.map((service) => (
            <ServiceCard key={service.id} service={service} featured />
          ))}
        </div>
        {extras.length > 0 && (
          <div className="service-extras">
            <div className="service-grid">
              {extras.map((service) => (
                <ServiceCard key={service.id} service={service} />
              ))}
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
