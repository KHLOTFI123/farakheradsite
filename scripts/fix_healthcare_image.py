import json
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:8000"
IMAGE = Path(r"C:\Users\khalil\.cursor\projects\c-farakheradsite\assets\healthcare-ai-cover.png")


def request(method, url, data=None, headers=None):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    with urllib.request.urlopen(req, timeout=60) as res:
        return json.loads(res.read())


token = request(
    "POST",
    f"{BASE}/api/auth/login",
    data=json.dumps({"username": "admin", "password": "admin123"}).encode(),
    headers={"Content-Type": "application/json"},
)["access_token"]

art = next(a for a in request("GET", f"{BASE}/api/articles") if a["slug"] == "healthcare-agentic-ai-2026")
boundary = "----FarakheradBoundaryFix"
body = (
    f"--{boundary}\r\n"
    'Content-Disposition: form-data; name="file"; filename="healthcare-ai-cover.png"\r\n'
    "Content-Type: image/png\r\n\r\n"
).encode() + IMAGE.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
url = request(
    "POST",
    f"{BASE}/api/admin/upload",
    data=body,
    headers={"Authorization": f"Bearer {token}", "Content-Type": f"multipart/form-data; boundary={boundary}"},
)["url"]
payload = {k: art[k] for k in ("title", "slug", "excerpt", "content")}
payload["image_url"] = url
out = request(
    "PUT",
    f"{BASE}/api/admin/articles/{art['id']}",
    data=json.dumps(payload, ensure_ascii=False).encode(),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
)
print(out["image_url"])
