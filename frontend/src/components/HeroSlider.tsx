import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { mediaUrl } from "../api";
import { useI18n } from "../i18n";
import type { Slide } from "../types";
import { IconArrow, IconChevron } from "./Icons";

export default function HeroSlider({ slides }: { slides: Slide[] }) {
  const [index, setIndex] = useState(0);
  const { to } = useI18n();

  useEffect(() => {
    if (slides.length < 2) return;
    const timer = window.setInterval(() => {
      setIndex((current) => (current + 1) % slides.length);
    }, 7000);
    return () => window.clearInterval(timer);
  }, [slides.length]);

  if (!slides.length) {
    return <section className="hero hero-loading" aria-hidden="true" />;
  }

  const slide = slides[index];

  return (
    <section className="hero">
      <div className="hero-bg" key={slide.id}>
        <img src={mediaUrl(slide.image_url)} alt="" />
      </div>
      <div className="container hero-slide">
        <div className="hero-copy">
          <h1>{slide.title}</h1>
          {slide.subtitle ? <p className="hero-lead">{slide.subtitle}</p> : null}
          <p>{slide.description}</p>
          <div className="hero-actions">
            <Link to={to(slide.cta_primary_link)} className="btn btn-gold">
              {slide.cta_primary_text}
              <IconArrow />
            </Link>
            <Link to={to(slide.cta_secondary_link)} className="btn btn-outline">
              {slide.cta_secondary_text}
              <IconArrow />
            </Link>
          </div>
        </div>
      </div>
      {slides.length > 1 && (
        <>
          <div className="hero-nav">
            <button
              type="button"
              className="prev"
              onClick={() => setIndex((i) => (i - 1 + slides.length) % slides.length)}
              aria-label="اسلاید قبل"
            >
              <IconChevron className="hero-chevron" />
            </button>
            <button
              type="button"
              className="next"
              onClick={() => setIndex((i) => (i + 1) % slides.length)}
              aria-label="اسلاید بعد"
            >
              <IconChevron className="hero-chevron" />
            </button>
          </div>
          <div className="hero-dots">
            {slides.map((item, dot) => (
              <button
                key={item.id}
                type="button"
                className={dot === index ? "active" : ""}
                aria-label={`${dot + 1}`}
                onClick={() => setIndex(dot)}
              />
            ))}
          </div>
        </>
      )}
    </section>
  );
}
