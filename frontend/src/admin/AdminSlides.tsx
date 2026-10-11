import { FormEvent, useEffect, useState } from "react";
import { api, mediaUrl } from "../api";
import type { Slide } from "../types";
import { uploadImage } from "./upload";

const empty: Omit<Slide, "id"> = {
  title: "",
  subtitle: "",
  description: "",
  image_url: "",
  cta_primary_text: "بیشتر بدانید",
  cta_primary_link: "/about",
  cta_secondary_text: "مشاهده محصولات",
  cta_secondary_link: "/products",
  sort_order: 1,
  is_active: true,
};

export default function AdminSlides() {
  const [slides, setSlides] = useState<Slide[]>([]);
  const [form, setForm] = useState(empty);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  function load() {
    api<Slide[]>("/api/admin/slides").then(setSlides).catch((err: Error) => setError(err.message));
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
        await api(`/api/admin/slides/${editingId}`, { method: "PUT", body: JSON.stringify(form) });
      } else {
        await api("/api/admin/slides", { method: "POST", body: JSON.stringify(form) });
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
    if (!window.confirm("این اسلاید حذف شود؟")) return;
    await api(`/api/admin/slides/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <div>
      <header className="admin-page-head">
        <div>
          <p className="admin-kicker">محتوا</p>
          <h1>اسلایدشو صفحه اول</h1>
          <p className="muted">اسلایدهای بالای صفحه اصلی را مدیریت کنید.</p>
        </div>
      </header>
      {error && <p className="error">{error}</p>}
      <form className="form" onSubmit={onSubmit} style={{ marginBottom: 28 }}>
        <input value={form.title} onChange={(e) => update("title", e.target.value)} placeholder="عنوان" required />
        <input value={form.subtitle} onChange={(e) => update("subtitle", e.target.value)} placeholder="زیرعنوان" />
        <textarea value={form.description} onChange={(e) => update("description", e.target.value)} placeholder="توضیح" />
        <input value={form.image_url} onChange={(e) => update("image_url", e.target.value)} placeholder="آدرس تصویر" />
        <input type="file" accept="image/*" onChange={(e) => onUpload(e.target.files?.[0])} />
        {form.image_url && <img src={mediaUrl(form.image_url)} alt="" style={{ height: 120, borderRadius: 12 }} />}
        <input value={form.cta_primary_text} onChange={(e) => update("cta_primary_text", e.target.value)} placeholder="متن دکمه اول" />
        <input value={form.cta_primary_link} onChange={(e) => update("cta_primary_link", e.target.value)} placeholder="لینک دکمه اول" />
        <input value={form.cta_secondary_text} onChange={(e) => update("cta_secondary_text", e.target.value)} placeholder="متن دکمه دوم" />
        <input value={form.cta_secondary_link} onChange={(e) => update("cta_secondary_link", e.target.value)} placeholder="لینک دکمه دوم" />
        <input type="number" value={form.sort_order} onChange={(e) => update("sort_order", Number(e.target.value))} placeholder="ترتیب" />
        <label>
          <input type="checkbox" checked={form.is_active} onChange={(e) => update("is_active", e.target.checked)} />
          نمایش در سایت
        </label>
        <button className="btn btn-gold" type="submit" disabled={saving}>
          {editingId ? "بروزرسانی اسلاید" : "افزودن اسلاید"}
        </button>
      </form>
      <table className="admin-table">
        <thead>
          <tr>
            <th>تصویر</th>
            <th>عنوان</th>
            <th>ترتیب</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {slides.map((slide) => (
            <tr key={slide.id}>
              <td>{slide.image_url && <img src={mediaUrl(slide.image_url)} alt="" />}</td>
              <td>
                <strong>{slide.title}</strong>
                <div className="muted">{slide.subtitle}</div>
              </td>
              <td>{slide.sort_order}</td>
              <td className="row-actions">
                <button className="btn btn-outline" type="button" onClick={() => { const { id, ...rest } = slide; setEditingId(id); setForm(rest); }}>ویرایش</button>
                <button className="btn btn-outline" type="button" onClick={() => remove(slide.id)}>حذف</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
