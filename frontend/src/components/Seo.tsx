import { useEffect } from "react";
import { useLocation } from "react-router-dom";
import { api } from "../api";
import { LOCALES, localeFromPath, type LocaleCode } from "../i18n";

type Hreflang = { lang: string; href: string };

type SeoMeta = {
  title: string;
  description?: string;
  keywords?: string;
  image?: string;
  site_url?: string;
  canonical?: string;
  robots?: string;
  lang?: string;
  dir?: "rtl" | "ltr";
  og_locale?: string;
  hreflang?: Hreflang[];
  jsonld?: unknown;
  found?: boolean;
};

function upsertMeta(attr: "name" | "property", key: string, value: string) {
  let node = document.head.querySelector(`meta[${attr}="${key}"]`) as HTMLMetaElement | null;
  if (!node) {
    node = document.createElement("meta");
    node.setAttribute(attr, key);
    document.head.appendChild(node);
  }
  node.setAttribute("content", value);
}

function upsertLink(rel: string, href: string, hreflang?: string) {
  const selector = hreflang
    ? `link[rel="${rel}"][hreflang="${hreflang}"]`
    : `link[rel="${rel}"]:not([hreflang])`;
  let node = document.head.querySelector(selector) as HTMLLinkElement | null;
  if (!node) {
    node = document.createElement("link");
    node.rel = rel;
    if (hreflang) node.hreflang = hreflang;
    document.head.appendChild(node);
  }
  node.href = href;
}

function clearHreflang() {
  document.head.querySelectorAll('link[rel="alternate"][hreflang]').forEach((node) => node.remove());
}

function applyMeta(meta: SeoMeta, path: string) {
  const origin = meta.site_url || window.location.origin;
  const canonical = meta.canonical || `${origin}${path}`;
  const description = meta.description || "";
  const image = meta.image?.startsWith("http") ? meta.image : `${origin}${meta.image || "/logo.png"}`;
  const robots = meta.robots || (meta.found === false ? "noindex, follow" : "index, follow");
  const locale = (meta.lang || localeFromPath(path)) as LocaleCode;
  const ogLocale = meta.og_locale || {
    fa: "fa_IR",
    "fa-AF": "fa_AF",
    en: "en_US",
    ar: "ar_SA",
    tr: "tr_TR",
    ru: "ru_RU",
  }[locale] || "fa_IR";

  document.title = meta.title;
  document.documentElement.lang = locale === "fa-AF" ? "fa-AF" : locale;
  document.documentElement.dir = meta.dir || (locale === "en" || locale === "tr" || locale === "ru" ? "ltr" : "rtl");

  upsertMeta("name", "description", description);
  if (meta.keywords) {
    upsertMeta("name", "keywords", meta.keywords);
  }
  upsertMeta("name", "robots", robots);
  upsertMeta("name", "googlebot", robots);
  upsertMeta("property", "og:title", meta.title);
  upsertMeta("property", "og:description", description);
  upsertMeta("property", "og:image", image);
  upsertMeta("property", "og:url", canonical);
  upsertMeta("property", "og:type", path.includes("/articles/") ? "article" : "website");
  upsertMeta("property", "og:locale", ogLocale);
  upsertMeta("property", "og:site_name", "Fara Kherad");
  upsertMeta("name", "twitter:card", "summary_large_image");
  upsertMeta("name", "twitter:title", meta.title);
  upsertMeta("name", "twitter:description", description);
  upsertMeta("name", "twitter:image", image);
  upsertLink("canonical", canonical);

  clearHreflang();
  const alternates = meta.hreflang?.length
    ? meta.hreflang
    : (() => {
        const bare = path.replace(/^\/(fa|en|ar|fa-AF|tr|ru)(?=\/|$)/, "") || "/";
        const list = LOCALES.map((item) => {
          const hrefPath = bare === "/" ? `/${item.code}` : `/${item.code}${bare}`;
          return { lang: item.code, href: `${origin}${hrefPath}` };
        });
        list.push({
          lang: "x-default",
          href: `${origin}${bare === "/" ? "/fa" : `/fa${bare}`}`,
        });
        return list;
      })();
  alternates.forEach((entry) => upsertLink("alternate", entry.href, entry.lang));

  document.querySelectorAll("script[data-seo-jsonld]").forEach((node) => node.remove());
  if (meta.jsonld) {
    const script = document.createElement("script");
    script.type = "application/ld+json";
    script.setAttribute("data-seo-jsonld", "true");
    script.text = JSON.stringify(meta.jsonld);
    document.head.appendChild(script);
  }
}

export default function Seo() {
  const location = useLocation();

  useEffect(() => {
    const path = location.pathname || "/";
    api<SeoMeta>(`/api/seo?path=${encodeURIComponent(path)}`)
      .then((meta) => applyMeta(meta, path))
      .catch(() => {
        applyMeta(
          {
            title: "فرا خرد | نرم‌افزار سازمانی و هوش مصنوعی",
            description: "فرا خرد توسعه‌دهنده نرم‌افزارهای سازمانی و راهکارهای هوش مصنوعی است.",
            robots: path.startsWith("/admin") ? "noindex, nofollow" : "index, follow",
          },
          path,
        );
      });
  }, [location.pathname]);

  return null;
}
