import json
import sqlite3
import urllib.request
from pathlib import Path

con = sqlite3.connect("/app/data/farakherad.db")
rows = con.execute(
    "SELECT key, value FROM site_settings WHERE key IN ('address','email','phone')"
).fetchall()
con.close()

out = {"db": rows, "api": {}}
for lang in ("fa", "en", "ar"):
    data = json.load(urllib.request.urlopen(f"http://127.0.0.1:8000/api/settings?lang={lang}"))
    items = data.get("items") or {}
    out["api"][lang] = items.get("address")

Path("/tmp/address_check.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
print("wrote")
