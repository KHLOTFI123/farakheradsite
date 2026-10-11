let apiLang = "fa";

export function setApiLang(lang: string) {
  apiLang = lang;
}

function withLang(path: string): string {
  if (path.startsWith("/api/admin") || path.startsWith("/api/auth")) return path;
  const join = path.includes("?") ? "&" : "?";
  return `${path}${join}lang=${encodeURIComponent(apiLang)}`;
}

function headers(extra?: HeadersInit, json = true): Headers {
  const result = new Headers(extra);
  const token = localStorage.getItem("token");
  if (json && !result.has("Content-Type")) {
    result.set("Content-Type", "application/json");
  }
  if (token) {
    result.set("Authorization", `Bearer ${token}`);
  }
  return result;
}

async function parseError(res: Response): Promise<string> {
  try {
    const data = await res.json();
    if (typeof data.detail === "string") return data.detail;
    if (Array.isArray(data.detail)) return data.detail.map((item: { msg?: string }) => item.msg).join(" ");
  } catch {
    /* ignore */
  }
  return "خطا در ارتباط با سرور";
}

export async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const isForm = options.body instanceof FormData;
  const hasJsonBody = options.body != null && !isForm;
  try {
    const res = await fetch(withLang(path), {
      ...options,
      headers: headers(options.headers, hasJsonBody),
    });
    if (!res.ok) {
      throw new Error(await parseError(res));
    }
    if (res.status === 204) {
      return undefined as T;
    }
    const contentType = res.headers.get("content-type") || "";
    if (!contentType.includes("application/json")) {
      throw new Error("خطا در ارتباط با سرور");
    }
    return res.json();
  } catch (err) {
    if (err instanceof Error) throw err;
    throw new Error("خطا در ارتباط با سرور");
  }
}

export function mediaUrl(url: string): string {
  if (!url) return "";
  if (url.startsWith("http")) return url;
  return url;
}
