
import sqlite3

conn = sqlite3.connect("D:/Business woman/SiteTasarimi/Arka uc (Backend)/veriler.db")
cursor = conn.cursor()

def add_site(site_adi: str):
    cursor.execute("""
        INSERT INTO "Site Detayları" ("Site Adı")
        VALUES (?)
    """, (site_adi,))
    conn.commit()
    print(f"Site eklendi: {site_adi}")

# Test
add_site("İstanbul Şantiye")
add_site("Ankara Şantiye")

for row in cursor.execute('SELECT * FROM "Site Detayları"'):
    print(row)

conn.close()



