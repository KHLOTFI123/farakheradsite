import { Navigate, Outlet, Route, Routes, useParams } from "react-router-dom";
import Layout from "./components/Layout";
import Seo from "./components/Seo";
import AdminArticles from "./admin/AdminArticles";
import AdminDashboard from "./admin/AdminDashboard";
import AdminLayout from "./admin/AdminLayout";
import AdminLogin from "./admin/AdminLogin";
import AdminMessages from "./admin/AdminMessages";
import AdminProducts from "./admin/AdminProducts";
import AdminServices from "./admin/AdminServices";
import AdminSlides from "./admin/AdminSlides";
import { isLocale } from "./i18n";
import About from "./pages/About";
import ArticleDetail from "./pages/ArticleDetail";
import Articles from "./pages/Articles";
import Contact from "./pages/Contact";
import Home from "./pages/Home";
import NotFound from "./pages/NotFound";
import ProductDetail from "./pages/ProductDetail";
import Products from "./pages/Products";
import Search from "./pages/Search";
import ServiceDetail from "./pages/ServiceDetail";
import Services from "./pages/Services";

function RootRedirect() {
  const saved = localStorage.getItem("lang");
  const lang = isLocale(saved || "") ? saved : "fa";
  return <Navigate to={`/${lang}`} replace />;
}

function LocaleGate() {
  const { lang } = useParams();
  if (!isLocale(lang)) return <NotFound />;
  return <Outlet />;
}

export default function App() {
  return (
    <>
      <Seo />
      <Routes>
        <Route path="/" element={<RootRedirect />} />
        <Route path="/admin/login" element={<AdminLogin />} />
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<AdminDashboard />} />
          <Route path="slides" element={<AdminSlides />} />
          <Route path="products" element={<AdminProducts />} />
          <Route path="services" element={<AdminServices />} />
          <Route path="articles" element={<AdminArticles />} />
          <Route path="messages" element={<AdminMessages />} />
        </Route>
        <Route path="/:lang" element={<LocaleGate />}>
          <Route element={<Layout />}>
            <Route index element={<Home />} />
            <Route path="products" element={<Products />} />
            <Route path="products/:slug" element={<ProductDetail />} />
            <Route path="services" element={<Services />} />
            <Route path="services/:slug" element={<ServiceDetail />} />
            <Route path="about" element={<About />} />
            <Route path="articles" element={<Articles />} />
            <Route path="articles/:slug" element={<ArticleDetail />} />
            <Route path="contact" element={<Contact />} />
            <Route path="search" element={<Search />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Route>
        <Route path="*" element={<NotFound />} />
      </Routes>
    </>
  );
}
