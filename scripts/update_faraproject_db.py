import json
import sqlite3
from pathlib import Path

payload = json.loads(Path("/tmp/_update_faraproject.json").read_text(encoding="utf-8"))
con = sqlite3.connect("/app/data/farakherad.db")
cur = con.cursor()
cur.execute(
    "UPDATE products SET image_url = ?, details = ?, description = ?, sort_order = ? WHERE slug = ?",
    (
        payload["image_url"],
        payload["details"],
        payload["description"],
        payload["sort_order"],
        "FaraProject",
    ),
)
print("rows", cur.rowcount)
con.commit()
row = con.execute(
    "SELECT slug, image_url, length(details), sort_order FROM products WHERE slug = ?",
    ("FaraProject",),
).fetchone()
print(row)
con.close()
