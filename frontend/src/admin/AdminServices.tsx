import { FormEvent, useEffect, useState } from "react";
import { api, mediaUrl } from "../api";
import { NamedIcon, SERVICE_ICONS } from "../components/Icons";
import type { ServiceItem } from "../types";
import { uploadImage } from "./upload";

const empty: Omit<ServiceItem, "id"> = {
  title: "",
  slug: "",
  description: "",
  icon: "star",
  image_url: "",
  sort_order: 1,
};

export default function AdminServices() {
  const [services, setServices] = useState<ServiceItem[]>([]);
  const [form, setForm] = useState(empty);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [error, setError] = useState("");
  const [saving, setSaving] = useState(false);

  function load() {
    api<ServiceItem[]>("/api/admin/services").then(setServices).catch((err: Error) => setError(err.message));
  }

  useEffect(load, []);

  function update<K extends keyof typeof empty>(key: K, value: (typeof empty)[K]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setSaving(true);
    setError("");
    const { details: _details, ...payload } = form;
    try {
      if (editingId) {
        await api(`/api/admin/services/${editingId}`, { method: "PUT", body: JSON.stringify(payload) });
      } else {
        await api("/api/admin/services", { method: "POST", body: JSON.stringify(payload) });
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
    if (!window.confirm("این خدمت حذف شود؟")) return;
    await api(`/api/admin/services/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <div className="admin-page">
      <header className="admin-page-head">
        <div>
          <p className="admin-kicker">محتوا</p>
          <h1>مدیریت خدمات</h1>
          <p className="muted">خدمات نمایش‌داده‌شده در صفحه اصلی و صفحه خدمات را از اینجا اضافه یا ویرایش کنید.</p>
        </div>
      </header>
      {error && <p className="error">{error}</p>}
      <form className="form admin-card" onSubmit={onSubmit}>
        <div className="admin-form-grid">
          <input value={form.title} onChange={(e) => update("title", e.target.value)} placeholder="عنوان خدمت" required />
          <input value={form.slug} onChange={(e) => update("slug", e.target.value)} placeholder="نامک انگلیسی مثل devops" required />
          <select value={form.icon} onChange={(e) => update("icon", e.target.value)}>
            {SERVICE_ICONS.map((name) => (
              <option key={name} value={name}>{name}</option>
            ))}
          </select>
          <input type="number" value={form.sort_order} onChange={(e) => update("sort_order", Number(e.target.value))} />
        </div>
        <textarea value={form.description} onChange={(e) => update("description", e.target.value)} placeholder="توضیح خدمت" required />
        <input value={form.image_url || ""} onChange={(e) => update("image_url", e.target.value)} placeholder="آدرس تصویر خدمت" />
        <input
          type="file"
          accept="image/*"
          onChange={async (e) => {
            const file = e.target.files?.[0];
            if (!file) return;
            try {
              update("image_url", await uploadImage(file));
            } catch (err) {
              setError(err instanceof Error ? err.message : "آپلود ناموفق بود");
            }
          }}
        />
        {form.image_url && <img src={mediaUrl(form.image_url)} alt="" style={{ height: 72, borderRadius: 10 }} />}
        <div className="admin-icon-preview">
          <NamedIcon name={form.icon} />
          <span>پیش‌نمایش آیکون</span>
        </div>
        <div className="row-actions">
          <button className="btn btn-gold" type="submit" disabled={saving}>
            {editingId ? "بروزرسانی خدمت" : "افزودن خدمت"}
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
            <th>آیکون</th>
            <th>خدمت</th>
            <th>ترتیب</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {services.map((service) => (
            <tr key={service.id}>
              <td>
                {service.image_url ? <img src={mediaUrl(service.image_url)} alt="" /> : "—"}
              </td>
              <td>
                <div className="icon-wrap">
                  <NamedIcon name={service.icon} />
                </div>
              </td>
              <td>
                <strong>{service.title}</strong>
                <div className="muted">{service.slug}</div>
                <div className="muted">{service.description}</div>
              </td>
              <td>{service.sort_order}</td>
              <td className="row-actions">
                <button
                  className="btn btn-outline"
                  type="button"
                  onClick={() => {
                    const { id, details: _details, ...rest } = service;
                    setEditingId(id);
                    setForm({ ...empty, ...rest });
                  }}
                >
                  ویرایش
                </button>
                <button className="btn btn-outline" type="button" onClick={() => remove(service.id)}>حذف</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
