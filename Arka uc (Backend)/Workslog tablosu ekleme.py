import sqlite3

# --- Bağlantı aç ---
conn = sqlite3.connect("D:/Business woman/SiteTasarimi/Arka uc (Backend)/veriler.db")
cursor = conn.cursor()

def add_all_worklogs():
    # Tüm çalışanları al
    cursor.execute("""
        SELECT "Çalışan ID", "Adı", "Site ID" FROM "Çalışan Detayları"
    """)
    calisanlar = cursor.fetchall()
    
    if not calisanlar:
        print("Hata: Çalışan bulunamadı.")
        return
    
    for calisan_id, adi, site_id in calisanlar:
        # Site adını al
        cursor.execute("""
            SELECT "Site Adı" FROM "Site Detayları" WHERE "Site ID" = ?
        """, (site_id,))
        site = cursor.fetchone()
        
        if site is None:
            print(f"Hata: Site ID {site_id} bulunamadı.")
            continue
        
        site_adi = site[0]
        
        # Workslog tablosuna ekle
        cursor.execute("""
            INSERT INTO workslog ("Çalışan ID", "Adı", "Site Adı", "Site ID")
            VALUES (?, ?, ?, ?)
        """, (calisan_id, adi, site_adi, site_id))
    
    conn.commit()
    print("Tüm çalışanların verileri workslog tablosuna eklendi.")

# --- Test çağrısı ---
add_all_worklogs()

conn.close()

