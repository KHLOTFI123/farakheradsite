import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { api } from "../api";
import { LogoMark } from "../components/Icons";

export default function AdminLogin() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await api<{ access_token: string }>("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ username, password }),
      });
      localStorage.setItem("token", data.access_token);
      navigate("/admin");
    } catch (err) {
      setError(err instanceof Error ? err.message : "ورود ناموفق بود");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login-page">
      <form className="login-card form" onSubmit={onSubmit}>
        <div className="admin-brand" style={{ justifyContent: "center", marginBottom: 8 }}>
          <LogoMark />
          <span>ورود به پنل مدیریت</span>
        </div>
        {error && <p className="error">{error}</p>}
        <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="نام کاربری" />
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="رمز عبور" />
        <button className="btn btn-gold" type="submit" disabled={loading}>
          {loading ? "در حال ورود..." : "ورود"}
        </button>
        <Link to="/" className="muted" style={{ textAlign: "center" }}>بازگشت به سایت</Link>
      </form>
    </div>
  );
}
