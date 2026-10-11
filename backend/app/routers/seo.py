import html
import json
from datetime import date, datetime, timezone
from urllib.parse import unquote

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, Response
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.i18n import LOCALES, RTL, localize_settings, present, split_lang
from app.models import Article, Product, Service, SiteSetting
from app.schemas import ArticleOut, ProductOut, ServiceOut

router = APIRouter(tags=["seo"])

OG_LOCALE = {
    "fa": "fa_IR",
    "fa-AF": "fa_AF",
    "en": "en_US",
    "ar": "ar_SA",
    "tr": "tr_TR",
    "ru": "ru_RU",
}

HTML_LANG = {
    "fa": "fa",
    "fa-AF": "fa-AF",
    "en": "en",
    "ar": "ar",
    "tr": "tr",
    "ru": "ru",
}

# Target keywords and SERP copy per product (primary: fa/en)
PRODUCT_SEO = {
    "enterprise-ai-platform": {
        "fa": {
            "title": "زیرساخت هوش مصنوعی سازمانی | پلتفرم GPU و LLM | {company}",
            "description": (
                "پلتفرم خصوصی هوش مصنوعی سازمانی فرا خرد: کلاستر GPU، سرو مدل، پایگاه برداری، "
                "مدیریت چرخه عمر LLM و استقرار On-Premise یا ابری برای سازمان‌های بزرگ."
            ),
            "keywords": (
                "زیرساخت هوش مصنوعی سازمانی, پلتفرم AI خصوصی, کلاستر GPU, سرو مدل LLM, "
                "پایگاه داده برداری, استقرار On-Premise هوش مصنوعی"
            ),
        },
        "en": {
            "title": "Enterprise AI Platform | Private GPU & LLM Infrastructure | {company}",
            "description": (
                "Fara Kherad private enterprise AI platform: GPU clusters, model serving, "
                "vector database, LLM lifecycle, and on-prem or cloud deployment."
            ),
            "keywords": (
                "enterprise AI platform, private AI infrastructure, GPU cluster, "
                "LLM serving, vector database, on-prem AI"
            ),
        },
    },
    "ai-assistant": {
        "fa": {
            "title": "دستیار هوش مصنوعی سازمانی | چت‌بات LLM و اتوماسیون | {company}",
            "description": (
                "دستیار هوشمند سازمانی فرا خرد مبتنی بر LLM: درک مکالمه، اتصال به سامانه‌ها، "
                "اتوماسیون فرایند و انجام وظایف چندمرحله‌ای برای تیم‌های کسب‌وکار."
            ),
            "keywords": (
                "دستیار هوش مصنوعی سازمانی, چت‌بات سازمانی, LLM, دستیار هوشمند کسب‌وکار, "
                "اتوماسیون با هوش مصنوعی, Agentic AI"
            ),
        },
        "en": {
            "title": "Enterprise AI Assistant | LLM Agent for Business | {company}",
            "description": (
                "Fara Kherad enterprise AI assistant: natural conversation, system integrations, "
                "process automation, and multi-step business actions powered by LLMs."
            ),
            "keywords": (
                "enterprise AI assistant, business chatbot, LLM agent, "
                "AI process automation, agentic AI"
            ),
        },
    },
    "intelligent-bi": {
        "fa": {
            "title": "هوش تجاری تعاملی | تحلیل داده با هوش مصنوعی بدون SQL | {company}",
            "description": (
                "هوش تجاری تعاملی فرا خرد: پرسش به فارسی یا انگلیسی، تولید امن SQL، "
                "جدول، نمودار و تحلیل برای تصمیم‌گیری مدیران بدون دانش فنی."
            ),
            "keywords": (
                "هوش تجاری تعاملی, BI مبتنی بر هوش مصنوعی, تحلیل داده بدون SQL, "
                "هوش تجاری سازمانی, Text to SQL"
            ),
        },
        "en": {
            "title": "Interactive BI | AI Data Analysis Without SQL | {company}",
            "description": (
                "Fara Kherad interactive BI: ask in plain language, generate safe SQL, "
                "and get tables, charts, and explanations for faster decisions."
            ),
            "keywords": (
                "interactive BI, AI business intelligence, text to SQL, "
                "enterprise analytics, natural language BI"
            ),
        },
    },
    "api-gateway": {
        "fa": {
            "title": "API Gateway سازمانی | امنیت، Rate Limit و صورتحساب API | {company}",
            "description": (
                "درگاه API سازمانی فرا خرد با احراز هویت، مسیریابی، محدودیت نرخ، مانیتورینگ، "
                "پیکربندی گرافیکی و موتور صورتحساب داخلی برای درآمدزایی از API."
            ),
            "keywords": (
                "API Gateway سازمانی, درگاه API, مدیریت API, Rate Limit, "
                "صورتحساب API, امنیت API"
            ),
        },
        "en": {
            "title": "Enterprise API Gateway | Auth, Rate Limits & Billing | {company}",
            "description": (
                "Fara Kherad enterprise API gateway with authentication, routing, rate limits, "
                "monitoring, visual setup, and built-in API billing."
            ),
            "keywords": (
                "enterprise API gateway, API management, rate limiting, "
                "API billing, API security"
            ),
        },
    },
    "online-queue-system": {
        "fa": {
            "title": "سامانه نوبت‌دهی آنلاین | مدیریت صف بیمارستان، بانک و سازمان | {company}",
            "description": (
                "سامانه نوبت‌دهی و مدیریت صف فرا خرد برای بیمارستان، کلینیک، بانک، بیمه و سازمان‌ها: "
                "رزرو آنلاین، صف زنده، پیامک و داشبورد چندشعبه."
            ),
            "keywords": (
                "سامانه نوبت‌دهی آنلاین, مدیریت صف, نوبت‌دهی بیمارستان, نوبت‌دهی بانک, "
                "نوبت‌دهی کلینیک, صف الکترونیکی"
            ),
        },
        "en": {
            "title": "Online Appointment & Queue System for Banks & Clinics | {company}",
            "description": (
                "Fara Kherad online booking and queue management for hospitals, clinics, banks, "
                "insurance, and public offices: live queues, SMS, and multi-branch control."
            ),
            "keywords": (
                "online appointment system, queue management software, hospital booking, "
                "bank queue system, clinic scheduling"
            ),
        },
    },
    "FaraProject": {
        "fa": {
            "title": "فراپروجکت | نرم‌افزار مدیریت پروژه، پورتفولیو و تسک سازمانی | {company}",
            "description": (
                "فراپروجکت سامانه یکپارچه مدیریت پورتفولیو، پروژه و تسک: برنامه‌ریزی، WBS، "
                "مدیریت منابع، پایش پیشرفت و گزارش مدیریتی برای PMO و مدیران پروژه."
            ),
            "keywords": (
                "نرم‌افزار مدیریت پروژه, مدیریت پورتفولیو, سامانه PMO, مدیریت تسک سازمانی, "
                "فراپروجکت, نرم‌افزار کنترل پروژه"
            ),
        },
        "en": {
            "title": "FaraProject | Portfolio, Project & Task Management Software | {company}",
            "description": (
                "FaraProject integrated portfolio, project, and task management: planning, WBS, "
                "resources, progress tracking, and executive reports for PMO teams."
            ),
            "keywords": (
                "project management software, portfolio management, PMO software, "
                "task management system, FaraProject"
            ),
        },
    },
}

SERVICE_SEO = {
    "devops": {
        "fa": {
            "title": "خدمات DevOps سازمانی | CI/CD، Kubernetes و اتوماسیون | {company}",
            "description": (
                "خدمات DevOps فرا خرد: طراحی CI/CD، Kubernetes، Docker، اتوماسیون زیرساخت "
                "و مانیتورینگ برای تحویل سریع‌تر و پایدارتر نرم‌افزار."
            ),
            "keywords": "خدمات DevOps, CI/CD, Kubernetes, Docker, اتوماسیون زیرساخت",
        },
        "en": {
            "title": "Enterprise DevOps Services | CI/CD & Kubernetes | {company}",
            "description": (
                "Fara Kherad DevOps services: CI/CD, Kubernetes, Docker, infrastructure automation, "
                "and monitoring for faster and safer software delivery."
            ),
            "keywords": "DevOps services, CI/CD, Kubernetes, Docker, infrastructure automation",
        },
    },
    "mlops": {
        "fa": {
            "title": "خدمات MLOps | استقرار مدل هوش مصنوعی و LLM | {company}",
            "description": (
                "خدمات MLOps فرا خرد برای چرخه عمر مدل، GPU، نسخه مدل، پایپ‌لاین آموزش "
                "و استقرار پایدار LLM در محیط سازمانی."
            ),
            "keywords": "خدمات MLOps, استقرار LLM, چرخه عمر مدل, GPU هوش مصنوعی, MLOps سازمانی",
        },
        "en": {
            "title": "MLOps Services | LLM Deployment & Model Lifecycle | {company}",
            "description": (
                "Fara Kherad MLOps services for model lifecycle, GPUs, training pipelines, "
                "and reliable LLM deployment in the enterprise."
            ),
            "keywords": "MLOps services, LLM deployment, model lifecycle, enterprise MLOps, AI GPU",
        },
    },
}

# Localized titles/descriptions for static marketing pages
PAGE_COPY = {
    "fa": {
        "home": {
            "title": "{company} | نرم‌افزار سازمانی و هوش مصنوعی",
            "description": (
                "شرکت فرا خرد؛ توسعه نرم‌افزار سازمانی، پلتفرم هوش مصنوعی، دستیار هوشمند، "
                "هوش تجاری، API Gateway، مدیریت پروژه و خدمات DevOps و MLOps در تهران."
            ),
            "heading": "هوش مصنوعی برای آینده کسب‌وکار شما",
            "body": None,
        },
        "products": {
            "title": "محصولات نرم‌افزاری و هوش مصنوعی سازمانی | {company}",
            "description": (
                "محصولات فرا خرد: زیرساخت هوش مصنوعی سازمانی، دستیار هوشمند، هوش تجاری تعاملی، "
                "API Gateway، سامانه نوبت‌دهی و فراپروجکت."
            ),
            "heading": "محصولات فرا خرد",
            "body": "راهکارهای هوش مصنوعی، زیرساخت سازمانی و نرم‌افزارهای تخصصی برای تحول دیجیتال.",
        },
        "services": {
            "title": "خدمات DevOps و MLOps سازمانی | {company}",
            "description": (
                "خدمات تخصصی فرا خرد برای CI/CD، Kubernetes، اتوماسیون زیرساخت، "
                "چرخه عمر مدل‌های هوش مصنوعی و استقرار LLM."
            ),
            "heading": "خدمات تخصصی زیرساخت و هوش مصنوعی",
            "body": "طراحی و پیاده‌سازی DevOps و MLOps برای سازمان‌های بزرگ.",
        },
        "about": {
            "title": "درباره {company} | شرکت فناوری اطلاعات و هوش مصنوعی",
            "description": None,
            "heading": None,
            "body": None,
        },
        "contact": {
            "title": "تماس با {company} | مشاوره نرم‌افزار و هوش مصنوعی",
            "description": "برای مشاوره رایگان نرم‌افزار سازمانی و هوش مصنوعی با فرا خرد در تهران تماس بگیرید.",
            "heading": "تماس با ما",
            "body": None,
        },
        "articles": {
            "title": "مقالات هوش مصنوعی سازمانی و DevOps | {company}",
            "description": "مقاله‌های تخصصی فرا خرد درباره هوش مصنوعی سازمانی، زیرساخت، DevOps و MLOps.",
            "heading": "مقالات",
            "body": "نکته‌ها و تجربه‌های تیم فرا خرد برای تحول دیجیتال سازمان‌ها.",
        },
        "search": {
            "title": "جستجو | {company}",
            "description": "جستجو در محصولات و مقالات فرا خرد.",
            "heading": "نتایج جستجو",
            "body": "",
        },
        "404": {
            "title": "صفحه پیدا نشد | {company}",
            "description": "صفحه مورد نظر در سایت فرا خرد موجود نیست.",
            "heading": "صفحه پیدا نشد",
            "body": "",
        },
    },
    "en": {
        "home": {
            "title": "{company} | Enterprise Software & Artificial Intelligence",
            "description": (
                "Fara Kherad builds enterprise software, private AI platforms, intelligent assistants, "
                "interactive BI, API gateways, project management, and DevOps/MLOps services."
            ),
            "heading": "Artificial intelligence for the next stage of your business",
            "body": None,
        },
        "products": {
            "title": "Enterprise AI & Software Products | {company}",
            "description": (
                "Explore Fara Kherad products: enterprise AI platform, AI assistant, interactive BI, "
                "API Gateway, queue system, and FaraProject."
            ),
            "heading": "Fara Kherad products",
            "body": "AI solutions, enterprise infrastructure, and specialized software.",
        },
        "services": {
            "title": "Enterprise DevOps & MLOps Services | {company}",
            "description": (
                "Fara Kherad DevOps and MLOps services: CI/CD, Kubernetes, infrastructure automation, "
                "model lifecycle, and LLM deployment."
            ),
            "heading": "Infrastructure and AI services",
            "body": "Design and run DevOps and MLOps for large organizations.",
        },
        "about": {
            "title": "About {company} | IT & Artificial Intelligence Company",
            "description": None,
            "heading": None,
            "body": None,
        },
        "contact": {
            "title": "Contact {company} | Enterprise AI Consultation",
            "description": "Contact Fara Kherad in Tehran for enterprise software and AI consultation.",
            "heading": "Contact us",
            "body": None,
        },
        "articles": {
            "title": "Enterprise AI & DevOps Articles | {company}",
            "description": "Articles from Fara Kherad on enterprise AI, infrastructure, DevOps, and MLOps.",
            "heading": "Articles",
            "body": "Practical notes from the Fara Kherad team.",
        },
        "search": {
            "title": "Search | {company}",
            "description": "Search Fara Kherad products and articles.",
            "heading": "Search results",
            "body": "",
        },
        "404": {
            "title": "Page not found | {company}",
            "description": "This page is not available on the Fara Kherad website.",
            "heading": "Page not found",
            "body": "",
        },
    },
}


def site_url() -> str:
    return settings.site_url.rstrip("/")


def setting_map(db: Session) -> dict[str, str]:
    return {row.key: row.value for row in db.query(SiteSetting).all()}


def _public_path(lang: str, bare: str) -> str:
    if bare in {"", "/"}:
        return f"/{lang}"
    return f"/{lang}{bare}"


def _absolute(url: str) -> str:
    if not url:
        return f"{site_url()}/logo.png"
    if url.startswith("http"):
        return url
    return f"{site_url()}{url}"


def _copy(lang: str, key: str) -> dict:
    if lang in PAGE_COPY:
        pack = PAGE_COPY[lang]
    elif lang in {"tr", "ru"}:
        pack = PAGE_COPY["en"]
    else:
        pack = PAGE_COPY["fa"]
    return dict(pack.get(key) or PAGE_COPY["fa"][key])


def _entity_seo(bucket: dict, slug: str, lang: str, company: str) -> dict:
    pack = bucket.get(slug) or {}
    if lang in pack:
        data = pack[lang]
    elif lang in {"tr", "ru"} and "en" in pack:
        data = pack["en"]
    elif "fa" in pack:
        data = pack["fa"]
    else:
        data = next(iter(pack.values()), {})
    return {
        "title": (data.get("title") or "").format(company=company),
        "description": data.get("description") or "",
        "keywords": data.get("keywords") or "",
    }


def _hreflang_entries(bare: str) -> list[dict[str, str]]:
    base = site_url()
    entries = []
    for lang in LOCALES:
        href = base + _public_path(lang, bare if bare != "/" else "/")
        entries.append({"lang": lang, "href": href})
    # x-default points to Persian as primary market
    entries.append({"lang": "x-default", "href": base + _public_path("fa", bare if bare != "/" else "/")})
    return entries


def _priority_for(bare: str) -> str:
    if bare in {"", "/"}:
        return "1.0"
    if bare in {"/products", "/services"}:
        return "0.9"
    if bare.startswith("/products/") or bare.startswith("/services/"):
        return "0.8"
    if bare.startswith("/articles"):
        return "0.7"
    if bare in {"/about", "/contact"}:
        return "0.6"
    return "0.5"


@router.get("/robots.txt", response_class=PlainTextResponse)
def robots():
    base = site_url()
    return (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin\n"
        "Disallow: /admin/\n"
        "Disallow: /api/\n"
        "Disallow: /*/search\n"
        "Disallow: /search\n"
        f"Sitemap: {base}/sitemap.xml\n"
        f"Host: {base.replace('https://', '').replace('http://', '')}\n"
    )


@router.get("/sitemap.xml")
def sitemap(db: Session = Depends(get_db)):
    base = site_url()
    today = date.today().isoformat()
    bare_paths = ["/", "/products", "/services", "/about", "/articles", "/contact"]
    lastmods: dict[str, str] = {path: today for path in bare_paths}

    for product in db.query(Product).filter(Product.is_active.is_(True)).all():
        path = f"/products/{product.slug}"
        bare_paths.append(path)
        lastmods[path] = today
    for service in db.query(Service).all():
        if service.slug:
            path = f"/services/{service.slug}"
            bare_paths.append(path)
            lastmods[path] = today
    for article in db.query(Article).all():
        path = f"/articles/{article.slug}"
        bare_paths.append(path)
        if article.published_at:
            lastmods[path] = article.published_at.date().isoformat()
        else:
            lastmods[path] = today

    chunks: list[str] = []
    for bare in bare_paths:
        for lang in LOCALES:
            loc = html.escape(base + _public_path(lang, bare))
            alts = []
            for entry in _hreflang_entries(bare):
                alts.append(
                    f'    <xhtml:link rel="alternate" hreflang="{html.escape(entry["lang"])}" '
                    f'href="{html.escape(entry["href"])}" />'
                )
            chunks.append(
                "  <url>\n"
                f"    <loc>{loc}</loc>\n"
                + "\n".join(alts)
                + "\n"
                f"    <lastmod>{lastmods.get(bare, today)}</lastmod>\n"
                f"    <changefreq>weekly</changefreq>\n"
                f"    <priority>{_priority_for(bare)}</priority>\n"
                "  </url>"
            )

    body = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(chunks)
        + "\n</urlset>\n"
    )
    return Response(content=body, media_type="application/xml")


def _org_jsonld(items: dict[str, str]) -> dict:
    base = site_url()
    linkedin = items.get("linkedin") or ""
    same_as = [linkedin] if linkedin.startswith("http") else []
    return {
        "@context": "https://schema.org",
        "@type": ["Organization", "ProfessionalService"],
        "@id": f"{base}/#organization",
        "name": items.get("company_name", "فرا خرد"),
        "alternateName": ["Fara Kherad", "Farakherad", "فراخرد"],
        "url": base,
        "logo": f"{base}/logo.png",
        "image": f"{base}/logo.png",
        "email": items.get("email") or None,
        "telephone": [t for t in [items.get("phone"), items.get("mobile")] if t],
        "address": {
            "@type": "PostalAddress",
            "addressLocality": "Tehran",
            "addressCountry": "IR",
            "streetAddress": items.get("address", "تهران، ایران"),
        },
        "areaServed": {"@type": "Country", "name": "Iran"},
        "description": items.get("about_text") or items.get("footer_text") or "",
        "sameAs": same_as,
        "knowsAbout": [
            "Artificial Intelligence",
            "Enterprise Software",
            "DevOps",
            "MLOps",
            "API Gateway",
            "Business Intelligence",
        ],
    }


def _website_jsonld(items: dict[str, str], lang: str) -> dict:
    base = site_url()
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{base}/#website",
        "url": f"{base}/{lang}",
        "name": items.get("company_name", "فرا خرد"),
        "inLanguage": HTML_LANG.get(lang, lang),
        "publisher": {"@id": f"{base}/#organization"},
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{base}/{lang}/search?q={{search_term_string}}",
            "query-input": "required name=search_term_string",
        },
    }


def _breadcrumb(lang: str, bare: str, title: str) -> dict | None:
    base = site_url()
    parts = [part for part in bare.split("/") if part]
    if not parts:
        return None
    labels = {
        "products": "Products" if lang == "en" else "محصولات",
        "services": "Services" if lang == "en" else "خدمات",
        "articles": "Articles" if lang == "en" else "مقالات",
        "about": "About" if lang == "en" else "درباره ما",
        "contact": "Contact" if lang == "en" else "تماس",
    }
    items = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home" if lang == "en" else "خانه",
            "item": f"{base}/{lang}",
        }
    ]
    trail = ""
    for index, part in enumerate(parts, start=2):
        trail += f"/{part}"
        name = title if part == parts[-1] else labels.get(part, part)
        items.append(
            {
                "@type": "ListItem",
                "position": index,
                "name": name,
                "item": f"{base}/{lang}{trail}",
            }
        )
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


def _page_meta(path: str, db: Session) -> dict:
    active_lang, bare = split_lang(path)
    items = localize_settings({"items": setting_map(db), "features": [], "stats": []}, active_lang)["items"]
    company = items.get("company_name", "فرا خرد")
    default_image = f"{site_url()}/logo.png"
    hero = f"{site_url()}/api/uploads/hero-ai.jpg"
    image = hero

    def pack(key: str) -> dict:
        data = _copy(active_lang, key)
        title = (data.get("title") or "").format(company=company)
        description = data.get("description")
        if description is None and key == "about":
            description = (items.get("about_text") or "")[:160]
        if description is None and key == "contact":
            description = (
                f"{company}: {items.get('phone', '')} | {items.get('address', 'تهران، ایران')}"
            )[:160]
        heading = data.get("heading")
        if heading is None and key == "about":
            heading = items.get("about_title", company)
        body = data.get("body")
        if body is None and key in {"home", "about"}:
            body = items.get("about_text") or description or ""
        if body is None and key == "contact":
            body = items.get("address") or "تهران، ایران"
        return {
            "title": title,
            "description": description or "",
            "image": image,
            "heading": heading or title,
            "body": body or "",
        }

    if bare in {"", "/"}:
        meta = pack("home")
        meta["image"] = hero
        return meta
    if bare == "/products":
        return pack("products")
    if bare == "/services":
        return pack("services")
    if bare == "/about":
        return pack("about")
    if bare == "/contact":
        return pack("contact")
    if bare == "/articles":
        return pack("articles")
    if bare == "/search":
        meta = pack("search")
        meta["robots"] = "noindex, follow"
        return meta
    if bare.startswith("/products/"):
        slug = unquote(bare.split("/", 2)[-1])
        product = db.query(Product).filter(Product.slug == slug, Product.is_active.is_(True)).first()
        if product:
            loc = present("products", ProductOut, product, active_lang)
            seo = _entity_seo(PRODUCT_SEO, product.slug, active_lang, company)
            desc = (seo.get("description") or loc.get("summary") or loc.get("description") or "")[:170]
            title = seo.get("title") or f"{loc['title']} | {company}"
            return {
                "title": title,
                "description": desc,
                "keywords": seo.get("keywords") or "",
                "image": _absolute(product.image_url),
                "heading": loc["title"],
                "body": loc.get("description") or desc,
                "found": True,
            }
        meta = pack("404")
        meta["found"] = False
        meta["robots"] = "noindex, follow"
        return meta
    if bare.startswith("/services/"):
        slug = unquote(bare.split("/", 2)[-1])
        service = db.query(Service).filter(Service.slug == slug).first()
        if service:
            loc = present("services", ServiceOut, service, active_lang)
            seo = _entity_seo(SERVICE_SEO, service.slug, active_lang, company)
            desc = (seo.get("description") or loc.get("description") or "")[:170]
            title = seo.get("title") or f"{loc['title']} | {company}"
            return {
                "title": title,
                "description": desc,
                "keywords": seo.get("keywords") or "",
                "image": _absolute(service.image_url) if service.image_url else default_image,
                "heading": loc["title"],
                "body": loc.get("description") or desc,
                "found": True,
            }
        meta = pack("404")
        meta["found"] = False
        meta["robots"] = "noindex, follow"
        return meta
    if bare.startswith("/articles/"):
        slug = unquote(bare.split("/", 2)[-1])
        article = db.query(Article).filter(Article.slug == slug).first()
        if article:
            loc = present("articles", ArticleOut, article, active_lang)
            return {
                "title": f"{loc['title']} | {company}",
                "description": (loc.get("excerpt") or "")[:160],
                "image": _absolute(article.image_url) if article.image_url else default_image,
                "heading": loc["title"],
                "body": loc.get("content") or loc.get("excerpt") or "",
                "found": True,
            }
        meta = pack("404")
        meta["found"] = False
        meta["robots"] = "noindex, follow"
        return meta
    if bare.startswith("/admin"):
        return {
            "title": "Admin",
            "description": "",
            "image": default_image,
            "heading": "Admin",
            "body": "",
            "robots": "noindex, nofollow",
        }
    meta = pack("404")
    meta["found"] = False
    meta["robots"] = "noindex, follow"
    return meta


def _product_jsonld(product: Product, items: dict[str, str], lang: str, localized: dict) -> list[dict]:
    base = site_url()
    details: dict = {}
    try:
        details = json.loads(product.details or "{}")
    except json.JSONDecodeError:
        details = {}
    url = f"{base}/{lang}/products/{product.slug}"
    seo = _entity_seo(PRODUCT_SEO, product.slug, lang, items.get("company_name", "فرا خرد"))
    schemas: list[dict] = [
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": localized.get("title") or product.title,
            "alternateName": seo.get("title") or None,
            "description": seo.get("description")
            or localized.get("summary")
            or product.summary
            or (product.description or "")[:220],
            "keywords": seo.get("keywords") or None,
            "image": _absolute(product.image_url),
            "url": url,
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Web",
            "inLanguage": HTML_LANG.get(lang, lang),
            "offers": {
                "@type": "Offer",
                "availability": "https://schema.org/InStock",
                "url": f"{base}/{lang}/contact",
            },
            "provider": {"@id": f"{base}/#organization"},
        }
    ]
    faqs = details.get("faqs") or []
    # Prefer localized FAQ overlay when English details exist via present(); details string may still be FA.
    if lang != "fa":
        try:
            overlay_details = json.loads(localized.get("details") or "{}")
            if overlay_details.get("faqs"):
                faqs = overlay_details["faqs"]
        except (TypeError, json.JSONDecodeError):
            pass
    if faqs:
        schemas.append(
            {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item["q"],
                        "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
                    }
                    for item in faqs
                    if item.get("q") and item.get("a")
                ],
            }
        )
    return schemas


def _service_jsonld(service: Service, lang: str, localized: dict, company: str = "فرا خرد") -> dict:
    base = site_url()
    seo = _entity_seo(SERVICE_SEO, service.slug, lang, company)
    return {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": localized.get("title") or service.title,
        "description": seo.get("description") or localized.get("description") or service.description,
        "keywords": seo.get("keywords") or None,
        "url": f"{base}/{lang}/services/{service.slug}",
        "provider": {"@id": f"{base}/#organization"},
        "areaServed": {"@type": "Country", "name": "Iran"},
        "serviceType": localized.get("title") or service.title,
        "image": _absolute(service.image_url) if service.image_url else f"{base}/logo.png",
    }


def _article_jsonld(article: Article, items: dict[str, str], lang: str, localized: dict) -> dict:
    base = site_url()
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": localized.get("title") or article.title,
        "description": localized.get("excerpt") or article.excerpt,
        "image": _absolute(article.image_url) if article.image_url else f"{base}/logo.png",
        "datePublished": article.published_at.isoformat() if article.published_at else None,
        "dateModified": article.published_at.isoformat() if article.published_at else datetime.now(timezone.utc).isoformat(),
        "inLanguage": HTML_LANG.get(lang, lang),
        "author": {"@id": f"{base}/#organization"},
        "publisher": {
            "@type": "Organization",
            "name": items.get("company_name", "فرا خرد"),
            "url": base,
            "logo": {"@type": "ImageObject", "url": f"{base}/logo.png"},
        },
        "mainEntityOfPage": f"{base}/{lang}/articles/{article.slug}",
    }


def _build_graphs(lang: str, bare: str, meta: dict, db: Session, items: dict[str, str]) -> list[dict]:
    graphs: list[dict] = [_org_jsonld(items), _website_jsonld(items, lang)]
    crumb = _breadcrumb(lang, bare if bare != "/" else "", meta.get("heading") or meta.get("title") or "")
    if crumb and bare not in {"", "/"}:
        graphs.append(crumb)
    if bare.startswith("/products/") and meta.get("found"):
        slug = unquote(bare.rsplit("/", 1)[-1])
        product = db.query(Product).filter(Product.slug == slug, Product.is_active.is_(True)).first()
        if product:
            loc = present("products", ProductOut, product, lang)
            graphs.extend(_product_jsonld(product, items, lang, loc))
    if bare.startswith("/services/") and meta.get("found"):
        slug = unquote(bare.rsplit("/", 1)[-1])
        service = db.query(Service).filter(Service.slug == slug).first()
        if service:
            loc = present("services", ServiceOut, service, lang)
            graphs.append(_service_jsonld(service, lang, loc, items.get("company_name", "فرا خرد")))
    if bare.startswith("/articles/") and meta.get("found"):
        slug = unquote(bare.rsplit("/", 1)[-1])
        article = db.query(Article).filter(Article.slug == slug).first()
        if article:
            loc = present("articles", ArticleOut, article, lang)
            graphs.append(_article_jsonld(article, items, lang, loc))
    return graphs


@router.get("/api/seo")
def seo_meta(path: str = "/", db: Session = Depends(get_db)):
    lang, bare = split_lang(path)
    public = path if path.startswith("/") else f"/{path}"
    if public == "/" or not public.split("/")[1:2] or public.split("/")[1] not in LOCALES:
        public = _public_path("fa", bare)
        lang = "fa"
    meta = _page_meta(public, db)
    items = localize_settings({"items": setting_map(db), "features": [], "stats": []}, lang)["items"]
    graphs = _build_graphs(lang, bare, meta, db, items)
    meta["site_url"] = site_url()
    meta["canonical"] = site_url() + public
    meta["lang"] = lang
    meta["dir"] = "rtl" if lang in RTL else "ltr"
    meta["og_locale"] = OG_LOCALE.get(lang, "fa_IR")
    meta["hreflang"] = _hreflang_entries(bare)
    meta["jsonld"] = graphs
    if meta.get("found") is False and "robots" not in meta:
        meta["robots"] = "noindex, follow"
    if not meta.get("image"):
        meta["image"] = f"{site_url()}/logo.png"
    else:
        meta["image"] = _absolute(meta["image"]) if not str(meta["image"]).startswith("http") else meta["image"]
    return meta


@router.get("/prerender", response_class=HTMLResponse)
def prerender(request: Request, db: Session = Depends(get_db)):
    path = request.headers.get("x-original-uri") or request.query_params.get("path") or "/"
    path = unquote(path.split("?", 1)[0])
    if path.startswith("/api/") or path.startswith("/assets/"):
        return HTMLResponse("", status_code=404)
    lang, bare = split_lang(path)
    public = path if path.split("/")[1:2] and path.split("/")[1] in LOCALES else _public_path("fa", bare)
    meta = _page_meta(public, db)
    items = localize_settings({"items": setting_map(db), "features": [], "stats": []}, lang)["items"]
    status = 404 if meta.get("found") is False else 200
    robots = meta.get("robots", "index, follow" if meta.get("found") is not False else "noindex, follow")
    base = site_url()
    canonical = base + public
    graphs = _build_graphs(lang, bare, meta, db, items)
    org = html.escape(json.dumps(graphs, ensure_ascii=False))
    products = db.query(Product).filter(Product.is_active.is_(True)).order_by(Product.sort_order).all()
    links = "".join(
        f'<li><a href="{html.escape(base)}/{html.escape(lang)}/products/{html.escape(item.slug)}">'
        f'{html.escape(present("products", ProductOut, item, lang)["title"])}</a></li>'
        for item in products
    )
    hreflang_tags = "".join(
        f'<link rel="alternate" hreflang="{html.escape(entry["lang"])}" href="{html.escape(entry["href"])}" />'
        for entry in _hreflang_entries(bare)
    )
    html_lang = HTML_LANG.get(lang, lang)
    html_dir = "rtl" if lang in RTL else "ltr"
    og_locale = OG_LOCALE.get(lang, "fa_IR")
    image = html.escape(_absolute(meta.get("image") or f"{base}/logo.png"))
    body = f"""<!doctype html>
<html lang="{html.escape(html_lang)}" dir="{html_dir}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(meta["title"])}</title>
  <meta name="description" content="{html.escape(meta.get("description") or "")}" />
  {f'<meta name="keywords" content="{html.escape(meta.get("keywords") or "")}" />' if meta.get("keywords") else ""}
  <meta name="robots" content="{html.escape(robots)}" />
  <link rel="canonical" href="{html.escape(canonical)}" />
  {hreflang_tags}
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="{html.escape(items.get("company_name", "فرا خرد"))}" />
  <meta property="og:title" content="{html.escape(meta["title"])}" />
  <meta property="og:description" content="{html.escape(meta.get("description") or "")}" />
  <meta property="og:image" content="{image}" />
  <meta property="og:url" content="{html.escape(canonical)}" />
  <meta property="og:locale" content="{html.escape(og_locale)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{html.escape(meta["title"])}" />
  <meta name="twitter:description" content="{html.escape(meta.get("description") or "")}" />
  <meta name="twitter:image" content="{image}" />
  <script type="application/ld+json">{org}</script>
</head>
<body>
  <header><a href="{html.escape(base)}/{html.escape(lang)}">{html.escape(items.get("company_name", "فرا خرد"))}</a></header>
  <main>
    <h1>{html.escape(meta.get("heading") or meta["title"])}</h1>
    <p>{html.escape((meta.get("body") or meta.get("description") or "")[:1200])}</p>
    <nav aria-label="products"><ul>{links}</ul></nav>
  </main>
</body>
</html>"""
    return HTMLResponse(content=body, status_code=status)
