import { FormEvent, useEffect, useState } from "react";
import { api, mediaUrl } from "../api";
import type { Article } from "../types";
import { uploadImage } from "./upload";

const empty = {
  title: "",
  slug: "",
  excerpt: "",
  content: "",
  image_url: "",
};

export default function AdminArticles() {
  const [articles, setArticles] = useState<Article[]>([]);
  const [form, setForm] = useState(empty);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  function load() {
    api<Article[]>("/api/admin/articles").then(setArticles).catch((err: Error) => setError(err.message));
  }

  useEffect(load, []);

  function update<K extends keyof typeof empty>(key: K, value: (typeof empty)[K]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  async function onUpload(file?: File) {
    if (!file) return;
    try {
      update("image_url", await uploadImage(file));
    } catch (err) {
      setError(err instanceof Error ? err.message : "آپلود ناموفق بود");
    }
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setSaving(true);
    setError("");
    try {
      if (editingId) {
        await api(`/api/admin/articles/${editingId}`, { method: "PUT", body: JSON.stringify(form) });
      } else {
        await api("/api/admin/articles", { method: "POST", body: JSON.stringify(form) });
      }
      setForm(empty);
      setEditingId(null);
      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "ذخیره ناموفق بود");
    } finally {
      setSaving(false);
    }
  }

  async function remove(id: number) {
    if (!window.confirm("این مقاله حذف شود؟")) return;
    await api(`/api/admin/articles/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <div className="admin-page">
      <header className="admin-page-head">
        <div>
          <p className="admin-kicker">محتوا</p>
          <h1>مدیریت مقالات</h1>
          <p className="muted">مقاله‌های سایت را اضافه کنید یا متن و تصویر آن‌ها را ویرایش کنید.</p>
        </div>
      </header>
      {error && <p className="error">{error}</p>}
      <form className="form admin-card" onSubmit={onSubmit}>
        <div className="admin-form-grid">
          <input value={form.title} onChange={(e) => update("title", e.target.value)} placeholder="عنوان مقاله" required />
          <input value={form.slug} onChange={(e) => update("slug", e.target.value)} placeholder="نامک انگلیسی مثل ai-benefits" required />
        </div>
        <input value={form.excerpt} onChange={(e) => update("excerpt", e.target.value)} placeholder="خلاصه کوتاه" />
        <textarea value={form.content} onChange={(e) => update("content", e.target.value)} placeholder="متن کامل مقاله" required />
        <input value={form.image_url} onChange={(e) => update("image_url", e.target.value)} placeholder="آدرس تصویر" />
        <input type="file" accept="image/*" onChange={(e) => onUpload(e.target.files?.[0])} />
        {form.image_url && <img src={mediaUrl(form.image_url)} alt="" style={{ height: 120, borderRadius: 12 }} />}
        <div className="row-actions">
          <button className="btn btn-gold" type="submit" disabled={saving}>
            {editingId ? "بروزرسانی مقاله" : "افزودن مقاله"}
          </button>
          {editingId && (
            <button className="btn btn-outline" type="button" onClick={() => { setEditingId(null); setForm(empty); }}>
              انصراف
            </button>
          )}
        </div>
      </form>
      <table className="admin-table">
        <thead>
          <tr>
            <th>تصویر</th>
            <th>مقاله</th>
            <th>نامک</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {articles.map((article) => (
            <tr key={article.id}>
              <td>{article.image_url && <img src={mediaUrl(article.image_url)} alt="" />}</td>
              <td>
                <strong>{article.title}</strong>
                <div className="muted">{article.excerpt}</div>
              </td>
              <td>{article.slug}</td>
              <td className="row-actions">
                <button
                  className="btn btn-outline"
                  type="button"
                  onClick={() => {
                    setEditingId(article.id);
                    setForm({
                      title: article.title,
                      slug: article.slug,
                      excerpt: article.excerpt,
                      content: article.content,
                      image_url: article.image_url,
                    });
                  }}
                >
                  ویرایش
                </button>
                <button className="btn btn-outline" type="button" onClick={() => remove(article.id)}>حذف</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
