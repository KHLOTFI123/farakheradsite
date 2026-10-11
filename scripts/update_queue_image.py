import sqlite3

con = sqlite3.connect("/app/data/farakherad.db")
cur = con.cursor()
cur.execute(
    "UPDATE products SET image_url = ? WHERE slug = ?",
    ("/api/uploads/queue-system-multi.jpg", "online-queue-system"),
)
print("rows", cur.rowcount)
con.commit()
print(
    con.execute(
        "SELECT slug, image_url FROM products WHERE slug = ?",
        ("online-queue-system",),
    ).fetchone()
)
con.close()
