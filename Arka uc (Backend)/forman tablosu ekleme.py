import sqlite3
from datetime import datetime

def ekle_forman(kullanici_adi, site_id, baslama_tarihi=None):
    conn = sqlite3.connect("veriler.db")  
    cursor = conn.cursor()

    if not baslama_tarihi:
        baslama_tarihi = datetime.now().strftime("%Y-%m-%d")

    cursor.execute("""SELECT "Site Adı" FROM "Site Detayları" WHERE "Site ID" = ?""", (site_id,))
    site = cursor.fetchone()

    if not site:
        print(f"❌ Hata: Site ID {site_id} bulunamadı.")
        conn.close()
        return

    site_adi = site[0]

    # Buradaki sütun isimleri tabloya uygun hale getirildi
    cursor.execute("""
        INSERT INTO "Forman" ("Kullancı Adı", "Site ID", "Site Adı", "Başlama Tarihi")
        VALUES (?, ?, ?, ?)
    """, (kullanici_adi, site_id, site_adi, baslama_tarihi))

    conn.commit()
    conn.close()
    print(f"✅ Foreman {kullanici_adi} ({site_adi}) tablosuna eklendi.")

# ---- Test ----
ekle_forman("Kadir", 1)
