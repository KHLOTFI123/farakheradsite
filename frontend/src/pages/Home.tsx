import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api, mediaUrl } from "../api";
import FeatureGrid from "../components/FeatureGrid";
import HeroSlider from "../components/HeroSlider";
import ProductCard from "../components/ProductCard";
import ServiceCard from "../components/ServiceCard";
import WhySection from "../components/WhySection";
import type { Article, Product, ServiceItem, SiteSettings, Slide } from "../types";
import { useI18n } from "../i18n";
import { isFeaturedService } from "../serviceUtils";

export default function Home() {
  const [slides, setSlides] = useState<Slide[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [services, setServices] = useState<ServiceItem[]>([]);
  const [articles, setArticles] = useState<Article[]>([]);
  const [settings, setSettings] = useState<SiteSettings | null>(null);
  const [error, setError] = useState("");
  const { lang, t, to } = useI18n();

  useEffect(() => {
    let cancelled = false;
    Promise.allSettled([
      api<Slide[]>("/api/slides"),
      api<Product[]>("/api/products"),
      api<ServiceItem[]>("/api/services"),
      api<Article[]>("/api/articles"),
      api<SiteSettings>("/api/settings"),
    ]).then(([slideData, productData, serviceData, articleData, settingData]) => {
      if (cancelled) return;
      if (slideData.status === "fulfilled") setSlides(slideData.value);
      if (productData.status === "fulfilled") setProducts(productData.value);
      if (serviceData.status === "fulfilled") setServices(serviceData.value);
      if (articleData.status === "fulfilled") setArticles(articleData.value);
      if (settingData.status === "fulfilled") setSettings(settingData.value);
      const allFailed = [slideData, productData, serviceData, articleData, settingData].every(
        (item) => item.status === "rejected",
      );
      if (allFailed) {
        const first = slideData.status === "rejected" ? slideData.reason : null;
        setError(first instanceof Error ? first.message : t("common.error"));
      }
    });
    return () => {
      cancelled = true;
    };
  }, [lang]);

  if (error) {
    return <div className="container section"><p className="error">{error}</p></div>;
  }

  return (
    <>
      <HeroSlider slides={slides} />
      {settings && <FeatureGrid features={settings.features} />}
      <section className="section">
        <div className="container">
          <div className="section-head">
            <div>
              <h2>{t("home.products")}</h2>
              <p>{t("home.productsLead")}</p>
            </div>
            <Link to={to("/products")} className="link-more">{t("home.moreProducts")}</Link>
          </div>
          <div className="product-grid">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} promo />
            ))}
          </div>
        </div>
      </section>
      <section className="section">
        <div className="container">
          <div className="section-head">
            <div>
              <h2>{t("home.services")}</h2>
              <p>{t("home.servicesLead")}</p>
            </div>
            <Link to={to("/services")} className="link-more">{t("home.moreServices")}</Link>
          </div>
          <div className="service-domains">
            {services.filter(isFeaturedService).map((service) => (
              <ServiceCard key={service.id} service={service} featured promo />
            ))}
          </div>
          {services.some((item) => !isFeaturedService(item)) && (
            <div className="service-grid" style={{ marginTop: 24 }}>
              {services.filter((item) => !isFeaturedService(item)).map((service) => (
                <ServiceCard key={service.id} service={service} promo />
              ))}
            </div>
          )}
        </div>
      </section>
      <section className="section">
        <div className="container">
          <div className="section-head">
            <div>
              <h2>{t("home.articles")}</h2>
              <p>{t("home.articlesLead")}</p>
            </div>
            <Link to={to("/articles")} className="link-more">{t("home.moreArticles")}</Link>
          </div>
          <ul className="home-article-titles">
            {articles.map((article) => (
              <li key={article.id}>
                <Link to={to(`/articles/${article.slug}`)}>
                  {article.image_url ? (
                    <img src={mediaUrl(article.image_url)} alt="" />
                  ) : null}
                  <span>{article.title}</span>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </section>
      {settings && (
        <section className="section">
          <WhySection settings={settings} />
        </section>
      )}
    </>
  );
}
