import { FormEvent, useEffect, useState } from "react";
import { api, mediaUrl } from "../api";
import type { Product } from "../types";
import { uploadImage } from "./upload";

const empty: Omit<Product, "id"> = {
  title: "",
  slug: "",
  summary: "",
  description: "",
  image_url: "",
  sort_order: 1,
  is_active: true,
};

export default function AdminProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [form, setForm] = useState(empty);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  function load() {
    api<Product[]>("/api/admin/products").then(setProducts).catch((err: Error) => setError(err.message));
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
        await api(`/api/admin/products/${editingId}`, { method: "PUT", body: JSON.stringify(form) });
      } else {
        await api("/api/admin/products", { method: "POST", body: JSON.stringify(form) });
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
    if (!window.confirm("این محصول حذف شود؟")) return;
    await api(`/api/admin/products/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <div className="admin-page">
      <header className="admin-page-head">
        <div>
          <p className="admin-kicker">محتوا</p>
          <h1>مدیریت محصولات</h1>
          <p className="muted">محصولات سایت را اضافه کنید، ویرایش کنید یا از نمایش خارج کنید.</p>
        </div>
      </header>
      {error && <p className="error">{error}</p>}
      <form className="form" onSubmit={onSubmit} style={{ marginBottom: 28 }}>
        <input value={form.title} onChange={(e) => update("title", e.target.value)} placeholder="نام محصول" required />
        <input value={form.slug} onChange={(e) => update("slug", e.target.value)} placeholder="نامک انگلیسی مثل ai-assistant" required />
        <input value={form.summary} onChange={(e) => update("summary", e.target.value)} placeholder="معرفی کوتاه" />
        <textarea value={form.description} onChange={(e) => update("description", e.target.value)} placeholder="معرفی کامل" />
        <input value={form.image_url} onChange={(e) => update("image_url", e.target.value)} placeholder="آدرس تصویر" />
        <input type="file" accept="image/*" onChange={(e) => onUpload(e.target.files?.[0])} />
        {form.image_url && <img src={mediaUrl(form.image_url)} alt="" style={{ height: 120, borderRadius: 12 }} />}
        <input type="number" value={form.sort_order} onChange={(e) => update("sort_order", Number(e.target.value))} />
        <label>
          <input type="checkbox" checked={form.is_active} onChange={(e) => update("is_active", e.target.checked)} />
          نمایش در سایت
        </label>
        <button className="btn btn-gold" type="submit" disabled={saving}>
          {editingId ? "بروزرسانی محصول" : "افزودن محصول"}
        </button>
      </form>
      <table className="admin-table">
        <thead>
          <tr>
            <th>تصویر</th>
            <th>محصول</th>
            <th>نامک</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {products.map((product) => (
            <tr key={product.id}>
              <td>{product.image_url && <img src={mediaUrl(product.image_url)} alt="" />}</td>
              <td>
                <strong>{product.title}</strong>
                <div className="muted">{product.summary}</div>
              </td>
              <td>{product.slug}</td>
              <td className="row-actions">
                <button className="btn btn-outline" type="button" onClick={() => { const { id, ...rest } = product; setEditingId(id); setForm(rest); }}>ویرایش</button>
                <button className="btn btn-outline" type="button" onClick={() => remove(product.id)}>حذف</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
