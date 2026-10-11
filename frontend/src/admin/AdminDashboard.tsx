import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import type { Article, Message, Product, ServiceItem, Slide } from "../types";

export default function AdminDashboard() {
  const [slides, setSlides] = useState<Slide[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [services, setServices] = useState<ServiceItem[]>([]);
  const [articles, setArticles] = useState<Article[]>([]);
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    Promise.allSettled([
      api<Slide[]>("/api/admin/slides"),
      api<Product[]>("/api/admin/products"),
      api<ServiceItem[]>("/api/admin/services"),
      api<Article[]>("/api/admin/articles"),
      api<Message[]>("/api/admin/messages"),
    ]).then(([s, p, v, a, m]) => {
      if (s.status === "fulfilled") setSlides(s.value);
      if (p.status === "fulfilled") setProducts(p.value);
      if (v.status === "fulfilled") setServices(v.value);
      if (a.status === "fulfilled") setArticles(a.value);
      if (m.status === "fulfilled") setMessages(m.value);
    });
  }, []);

  const unread = messages.filter((item) => !item.is_read).length;

  return (
    <div className="admin-page">
      <header className="admin-page-head">
        <div>
          <p className="admin-kicker">خوش آمدید</p>
          <h1>خلاصه پنل</h1>
          <p className="muted">وضعیت محتوا و پیام‌های سایت فرا خرد را از اینجا ببینید.</p>
        </div>
      </header>
      <div className="admin-stat-grid">
        <article className="admin-stat"><strong>{slides.length}</strong><span>اسلاید</span></article>
        <article className="admin-stat"><strong>{products.length}</strong><span>محصول</span></article>
        <article className="admin-stat"><strong>{services.length}</strong><span>خدمت</span></article>
        <article className="admin-stat"><strong>{articles.length}</strong><span>مقاله</span></article>
        <article className="admin-stat"><strong>{unread}</strong><span>پیام خوانده‌نشده</span></article>
      </div>
      <div className="admin-quick">
        <Link to="/admin/slides" className="admin-card-link">مدیریت اسلایدشو</Link>
        <Link to="/admin/products" className="admin-card-link">ویرایش محصولات</Link>
        <Link to="/admin/services" className="admin-card-link">ویرایش خدمات</Link>
        <Link to="/admin/articles" className="admin-card-link">ویرایش مقالات</Link>
        <Link to="/admin/messages" className="admin-card-link">صندوق پیام</Link>
      </div>
    </div>
  );
}
