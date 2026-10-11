import { Link } from "react-router-dom";
import { mediaUrl } from "../api";
import { useI18n } from "../i18n";
import type { ServiceItem } from "../types";
import { IconArrow, NamedIcon } from "./Icons";

const FALLBACK_IMAGES: Record<string, string> = {
  devops: "/images/service-devops.jpg",
  mlops: "/images/service-mlops.jpg",
  "خدمات DevOps": "/images/service-devops.jpg",
  "خدمات MLOps": "/images/service-mlops.jpg",
};

function imageSrc(service: ServiceItem) {
  return service.image_url || FALLBACK_IMAGES[service.slug] || FALLBACK_IMAGES[service.title] || "";
}

export default function ServiceCard({
  service,
  featured = false,
  promo = false,
}: {
  service: ServiceItem;
  featured?: boolean;
  promo?: boolean;
}) {
  const { t, to } = useI18n();
  const src = imageSrc(service);
  const href = to(service.slug ? `/services/${service.slug}` : "/services");
  const promoLabel = promo ? <span className="price-promo">Prices – Limited Time Only</span> : null;

  if (featured) {
    return (
      <article className="service-card service-domain">
        {src ? (
          <div className="card-media">
            <img src={mediaUrl(src)} alt={service.title} />
            {promoLabel}
          </div>
        ) : (
          promoLabel
        )}
        <div className="body">
          <h3>{service.title}</h3>
          <p>{service.description}</p>
          <Link to={href} className="link-more">
            {t("service.more")}
            <IconArrow />
          </Link>
        </div>
      </article>
    );
  }

  return (
    <article className="service-card">
      {promoLabel}
      <div className="service-card-head">
        {src ? (
          <img className="service-thumb" src={mediaUrl(src)} alt="" />
        ) : (
          <div className="icon-wrap">
            <NamedIcon name={service.icon} />
          </div>
        )}
        <h3>{service.title}</h3>
      </div>
      <p>{service.description}</p>
      {service.slug ? (
        <Link to={href} className="link-more">
          {t("service.more")}
          <IconArrow />
        </Link>
      ) : null}
    </article>
  );
}
