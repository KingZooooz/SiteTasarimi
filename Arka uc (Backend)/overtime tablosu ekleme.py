import sqlite3
from datetime import datetime

def ekle_overtime(calisan_id, site_id, saat, tarih=None):
    conn = sqlite3.connect("veriler.db")  # veritabanı dosya yolunu kendine göre ayarla
    cursor = conn.cursor()

    # Tarih boşsa bugünün tarihi
    if not tarih:
        tarih = datetime.now().strftime("%Y-%m-%d")

    # Çalışan adını al
    cursor.execute("""SELECT "Adı" FROM "Çalışan Detayları" WHERE "Çalışan ID" = ?""", (calisan_id,))
    calisan = cursor.fetchone()
    if not calisan:
        print(f"❌ Hata: Çalışan ID {calisan_id} bulunamadı.")
        conn.close()
        return
    calisan_adi = calisan[0]

    # Site adını al
    cursor.execute("""SELECT "Site Adı" FROM "Site Detayları" WHERE "Site ID" = ?""", (site_id,))
    site = cursor.fetchone()
    if not site:
        print(f"❌ Hata: Site ID {site_id} bulunamadı.")
        conn.close()
        return
    site_adi = site[0]

    # Overtime tablosuna ekle
    cursor.execute("""
        INSERT INTO "Overtime" ("Çalışan ID", "Çalışan Adı", "Site ID", "Site Adı", "Saat", "Tarih")
        VALUES (?, ?, ?, ?, ?, ?)
    """, (calisan_id, calisan_adi, site_id, site_adi, saat, tarih))

    conn.commit()
    conn.close()
    print(f"✅ Overtime eklendi: {calisan_adi} ({site_adi}) - Saat: {saat}, Tarih: {tarih}")

# ---- Test ----
ekle_overtime(1, 1, "20:00")  # Çalışan ID 1, Site ID 1 için overtime ekler
