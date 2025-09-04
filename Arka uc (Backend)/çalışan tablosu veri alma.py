import sqlite3

conn = sqlite3.connect("D:/Business woman/SiteTasarimi/Arka uc (Backend)/veriler.db")
cursor = conn.cursor()

# Tüm çalışanları al
cursor.execute("SELECT * FROM 'Çalışan Detayları'")
calisanlar = cursor.fetchall()

print("----- Çalışan Detayları -----")
for calisan in calisanlar:
    print(f"Çalışan ID: {calisan[0]}, Adı: {calisan[1]}, Yaş: {calisan[2]}, Durum: {calisan[3]}, Maaş: {calisan[4]}, Site ID: {calisan[5]}")

conn.close()
