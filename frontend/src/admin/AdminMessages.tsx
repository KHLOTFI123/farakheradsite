import { useEffect, useState } from "react";
import { api } from "../api";
import type { Message } from "../types";

export default function AdminMessages() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [error, setError] = useState("");

  function load() {
    api<Message[]>("/api/admin/messages").then(setMessages).catch((err: Error) => setError(err.message));
  }

  useEffect(load, []);

  async function markRead(id: number) {
    await api(`/api/admin/messages/${id}/read`, { method: "PATCH" });
    load();
  }

  async function remove(id: number) {
    if (!window.confirm("این پیام حذف شود؟")) return;
    await api(`/api/admin/messages/${id}`, { method: "DELETE" });
    load();
  }

  return (
    <div className="admin-page">
      <header className="admin-page-head">
        <div>
          <p className="admin-kicker">ارتباط</p>
          <h1>پیام‌های دریافت‌شده</h1>
          <p className="muted">درخواست‌های فرم تماس را بخوانید و پیگیری کنید.</p>
        </div>
      </header>
      {error && <p className="error">{error}</p>}
      <table className="admin-table">
        <thead>
          <tr>
            <th>فرستنده</th>
            <th>موضوع</th>
            <th>متن</th>
            <th>وضعیت</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {messages.map((message) => (
            <tr key={message.id}>
              <td>
                <strong>{message.name}</strong>
                <div className="muted">{message.email}</div>
                <div className="muted">{message.phone}</div>
              </td>
              <td>{message.subject}</td>
              <td>{message.body}</td>
              <td>
                <span className={`badge ${message.is_read ? "read" : ""}`}>
                  {message.is_read ? "خوانده‌شده" : "جدید"}
                </span>
              </td>
              <td className="row-actions">
                {!message.is_read && (
                  <button className="btn btn-outline" type="button" onClick={() => markRead(message.id)}>علامت خوانده</button>
                )}
                <button className="btn btn-outline" type="button" onClick={() => remove(message.id)}>حذف</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {messages.length === 0 && <p className="muted">هنوز پیامی دریافت نشده است.</p>}
    </div>
  );
}
