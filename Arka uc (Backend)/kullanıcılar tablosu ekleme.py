import sqlite3
from datetime import datetime

# --- Bağlantıyı aç ---
conn = sqlite3.connect("veriler.db")
cursor = conn.cursor()

# --- Fonksiyon ---
def ekle_kullanici(kullanici_adi, kullanici_tipi, site_id=None, baslama_tarihi=None):
    if not baslama_tarihi:
        baslama_tarihi = datetime.now().strftime("%Y-%m-%d")
    
    # Kullanıcıyı ekle
    cursor.execute("""
        INSERT INTO "Kullanıcılar" ("Kullanıcı_Adi", "Kullanıcı_tipi", "Baslama_Tarihi")
        VALUES (?, ?, ?)
    """, (kullanici_adi, kullanici_tipi, baslama_tarihi))
    conn.commit()
    print(f"✅ Kullanıcı eklendi: {kullanici_adi} ({kullanici_tipi})")
    
    # Eğer kullanıcı tipi Forman ise Forman tablosuna ekle
    if kullanici_tipi.lower() == "forman":
        if not site_id:
            print("❌ Hata: Forman eklemek için Site_ID gerekli.")
            return
        
        # Site adını çek
        cursor.execute("""SELECT "Site Adı" FROM "Site Detayları" WHERE "Site ID" = ?""", (site_id,))
        site = cursor.fetchone()
        if not site:
            print(f"❌ Hata: Site ID {site_id} bulunamadı.")
            return
        site_adi = site[0]

        cursor.execute("""
            INSERT INTO "Forman" ("Kullanıcı_Adi", "Site_ID", "Site_Adi", "Baslama_Tarihi")
            VALUES (?, ?, ?, ?)
        """, (kullanici_adi, site_id, site_adi, baslama_tarihi))
        conn.commit()
        print(f"✅ Forman tablosuna eklendi: {kullanici_adi} ({site_adi})")

# --- Test ---
ekle_kullanici("Ahmet Yılmaz", "Forman", site_id=1)
ekle_kullanici("Elif Aksoy", "Engineer")
conn.close()
