import { FormEvent, useState } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";
import { LOCALES, useI18n, useSwitchLang, type LocaleCode } from "../i18n";
import { useSite } from "../siteContext";
import { IconMenu, IconSearch, IconUser, IconX, LogoMark } from "./Icons";

const links = [
  { to: "/", key: "nav.home" },
  { to: "/products", key: "nav.products" },
  { to: "/services", key: "nav.services" },
  { to: "/about", key: "nav.about" },
  { to: "/articles", key: "nav.articles" },
  { to: "/contact", key: "nav.contact" },
];

export default function Header() {
  const navigate = useNavigate();
  const { items } = useSite();
  const { t, to, lang } = useI18n();
  const switchLang = useSwitchLang();
  const [query, setQuery] = useState("");
  const [open, setOpen] = useState(false);

  function onSearch(event: FormEvent) {
    event.preventDefault();
    const q = query.trim();
    if (q) {
      navigate(to(`/search?q=${encodeURIComponent(q)}`));
      setOpen(false);
    }
  }

  const mainLinks = links.filter((link) => link.to !== "/contact");

  return (
    <header className="site-header">
      <div className="util-bar">
        <div className="container util-inner">
          <span className="util-note">{items.tagline}</span>
          <div className="util-links">
            <form className="search-box" onSubmit={onSearch}>
              <IconSearch />
              <input
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={t("search.placeholder")}
                aria-label={t("search.placeholder")}
              />
            </form>
            <Link to="/admin/login">{t("header.login")}</Link>
          </div>
        </div>
      </div>
      <div className="container header-inner">
        <Link to={to("/")} className="brand" aria-label={items.company_name || "فرا خرد"}>
          <LogoMark />
        </Link>
        <nav className="nav">
          {mainLinks.map((link) => (
            <NavLink key={link.to} to={to(link.to)} end={link.to === "/"}>
              {t(link.key)}
            </NavLink>
          ))}
        </nav>
        <div className="header-actions">
          <label className="lang-switch">
            <span className="sr-only">{lang}</span>
            <select value={lang} onChange={(event) => switchLang(event.target.value as LocaleCode)} aria-label={lang}>
              {LOCALES.map((item) => (
                <option key={item.code} value={item.code}>{item.label}</option>
              ))}
            </select>
          </label>
          <Link to={to("/contact")} className="btn btn-gold">
            {t("nav.contact")}
          </Link>
          <button className="menu-toggle" type="button" onClick={() => setOpen((v) => !v)} aria-label={t("header.menu")}>
            {open ? <IconX className="icon" /> : <IconMenu className="icon" />}
          </button>
        </div>
      </div>
      <nav className={`container mobile-nav ${open ? "open" : ""}`}>
        {links.map((link) => (
          <NavLink key={link.to} to={to(link.to)} end={link.to === "/"} onClick={() => setOpen(false)}>
            {t(link.key)}
          </NavLink>
        ))}
        <form className="search-box" onSubmit={onSearch}>
          <IconSearch />
          <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder={t("search.placeholder")} />
        </form>
      </nav>
    </header>
  );
}
