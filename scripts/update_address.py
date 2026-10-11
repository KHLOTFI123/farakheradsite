import sqlite3

con = sqlite3.connect("/app/data/farakherad.db")
cur = con.cursor()
cur.execute("UPDATE site_settings SET value = ? WHERE key = ?", ("تهران، ایران", "address"))
print("address rows", cur.rowcount)
con.commit()
print(con.execute("SELECT key, value FROM site_settings WHERE key IN ('address','email')").fetchall())
con.close()
