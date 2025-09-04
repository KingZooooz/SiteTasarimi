import sqlite3

# Veritabanı dosyasına bağlan
conn = sqlite3.connect("D:/Business woman/SiteTasarimi/Arka uc (Backend)/veriler.db")
cursor = conn.cursor()

# Kullanıcıdan veri al
adi = input("Çalışan Adı: ")
yas = int(input("Yaş: "))
durum = input("Durum (Aktif/Pasif): ")
maas = float(input("Maaş: "))

# Site tablosundaki mevcut siteleri listele
print("\nMevcut Siteler:")
cursor.execute('SELECT "Site ID", "Site Adı" FROM "Site Detayları"')
siteler = cursor.fetchall()
for s in siteler:
    print(f"{s[0]} - {s[1]}")

site_id = int(input("Çalışanın bağlı olduğu Site ID'yi seç: "))

# Çalışan Detayları tablosuna ekle
try:
    cursor.execute("""
        INSERT INTO "Çalışan Detayları" ("Adı", "Yaş", "Durum", "Maaş", "Site ID")
        VALUES (?, ?, ?, ?, ?)
    """, (adi, yas, durum, maas, site_id))

    conn.commit()
    print("✅ Çalışan başarıyla eklendi.")
except sqlite3.Error as e:
    print("❌ Veri eklenirken hata oluştu:", e)

# Bağlantıyı kapat
conn.close()

