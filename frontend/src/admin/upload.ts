import { api } from "../api";

export async function uploadImage(file: File): Promise<string> {
  const body = new FormData();
  body.append("file", file);
  const data = await api<{ url: string }>("/api/admin/upload", { method: "POST", body });
  return data.url;
}
