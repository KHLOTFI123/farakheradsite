import { FormEvent, useState } from "react";
import { api } from "../api";
import { useI18n } from "../i18n";
import { useSite } from "../siteContext";

export default function Contact() {
  const { items } = useSite();
  const { t } = useI18n();
  const [form, setForm] = useState({ name: "", email: "", phone: "", subject: "", body: "" });
  const [status, setStatus] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function update(key: string, value: string) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setStatus("");
    try {
      await api("/api/contact", { method: "POST", body: JSON.stringify(form) });
      setStatus(t("contact.ok"));
      setForm({ name: "", email: "", phone: "", subject: "", body: "" });
    } catch (err) {
      setError(err instanceof Error ? err.message : t("contact.fail"));
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="section">
      <div className="container" style={{ maxWidth: 860 }}>
        <div className="page-hero">
          <h1>{t("contact.title")}</h1>
          <p className="muted">{t("contact.lead")}</p>
        </div>
        <div className="detail">
          <form className="form" onSubmit={onSubmit}>
            {status && <p className="success">{status}</p>}
            {error && <p className="error">{error}</p>}
            <input value={form.name} onChange={(e) => update("name", e.target.value)} placeholder={t("contact.name")} required />
            <input type="email" value={form.email} onChange={(e) => update("email", e.target.value)} placeholder={t("contact.email")} required />
            <input value={form.phone} onChange={(e) => update("phone", e.target.value)} placeholder={t("contact.phone")} />
            <input value={form.subject} onChange={(e) => update("subject", e.target.value)} placeholder={t("contact.subject")} />
            <textarea value={form.body} onChange={(e) => update("body", e.target.value)} placeholder={t("contact.body")} required />
            <button className="btn btn-gold" type="submit" disabled={loading}>
              {loading ? t("contact.sending") : t("contact.send")}
            </button>
          </form>
          <div className="content-card" style={{ padding: 24 }}>
            <h3>{t("contact.info")}</h3>
            <p>{t("contact.emailLabel")}: {items.email || "info@farakherad.com"}</p>
            <p>{t("contact.phoneLabel")}: {items.phone || "02177132703"}</p>
            <p>{t("contact.mobileLabel")}: {items.mobile || "09121788139"}</p>
            <p>{t("contact.addressLabel")}: {items.address}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
