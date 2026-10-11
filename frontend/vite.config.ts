import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

const backend = "http://127.0.0.1:8000";
const proxy = {
  "/api": { target: backend, changeOrigin: true },
  "/robots.txt": { target: backend, changeOrigin: true },
  "/sitemap.xml": { target: backend, changeOrigin: true },
};

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy,
  },
  preview: {
    port: 4173,
    proxy,
  },
});
