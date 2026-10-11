import { Navigate, NavLink, Outlet, useNavigate } from "react-router-dom";
import { LogoMark } from "../components/Icons";

const links = [
  { to: "/admin", label: "خلاصه", end: true },
  { to: "/admin/slides", label: "اسلایدشو" },
  { to: "/admin/products", label: "محصولات" },
  { to: "/admin/services", label: "خدمات" },
  { to: "/admin/articles", label: "مقالات" },
  { to: "/admin/messages", label: "پیام‌ها" },
];

export default function AdminLayout() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  if (!token) {
    return <Navigate to="/admin/login" replace />;
  }

  function logout() {
    localStorage.removeItem("token");
    navigate("/admin/login");
  }

  return (
    <div className="admin-shell">
      <aside className="admin-side">
        <div className="admin-brand">
          <LogoMark />
          <span>پنل مدیریت</span>
        </div>
        <nav className="admin-nav">
          {links.map((item) => (
            <NavLink key={item.to} to={item.to} end={item.end}>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="admin-side-foot">
          <NavLink to="/">مشاهده سایت</NavLink>
          <button type="button" onClick={logout}>خروج</button>
        </div>
      </aside>
      <div className="admin-main">
        <Outlet />
      </div>
    </div>
  );
}
