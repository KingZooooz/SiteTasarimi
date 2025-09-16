import sqlite3
from datetime import datetime

# --- Bağlantı aç ---
conn = sqlite3.connect("veriler.db")
cursor = conn.cursor()

# --- Fonksiyon ---
def ekle_worklog(calisan_id, site_id, saat=None, tarih=None):
    if not tarih:
        tarih = datetime.now().strftime("%Y-%m-%d")
    if not saat:
        saat = datetime.now().strftime("%H:%M:%S")
    
    # Aynı çalışan ve tarih için kayıt var mı kontrol et
    cursor.execute("""
        SELECT * FROM "Worklogs"
        WHERE "Çalışan_ID" = ? AND "Tarih" = ?
    """, (calisan_id, tarih))
    
    mevcut = cursor.fetchone()
    if mevcut:
        print(f"❌ Hata: Bu tarihte mevcut olan bir worklog var!! (Çalışan ID {calisan_id}, Tarih {tarih})")
        return
    
    # Çalışan adını çek
    cursor.execute("""SELECT "Kullanıcı_Adi" FROM "Kullanıcılar" WHERE "ID" = ?""", (calisan_id,))
    calisan = cursor.fetchone()
    if not calisan:
        print(f"❌ Hata: Çalışan ID {calisan_id} bulunamadı.")
        return
    calisan_adi = calisan[0]
    
    # Site adını çek
    cursor.execute("""SELECT "Site Adı" FROM "Site Detayları" WHERE "Site ID" = ?""", (site_id,))
    site = cursor.fetchone()
    if not site:
        print(f"❌ Hata: Site ID {site_id} bulunamadı.")
        return
    site_adi = site[0]
    
    # Worklog ekle
    cursor.execute("""
        INSERT INTO "Worklogs" ("Çalışan_ID", "Çalışan_Adi", "Site_ID", "Site_Adi", "Saat", "Tarih")
        VALUES (?, ?, ?, ?, ?, ?)
    """, (calisan_id, calisan_adi, site_id, site_adi, saat, tarih))
    conn.commit()
    print(f"✅ Worklog eklendi: {calisan_adi} ({site_adi}) - {tarih} {saat}")

# --- Test ---
ekle_worklog(1, 1)
# ekle_worklog(2, 2, "15:30:00", "2025-09-16")

# conn.close()
