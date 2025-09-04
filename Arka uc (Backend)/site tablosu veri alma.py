import sqlite3

conn = sqlite3.connect("D:/Business woman/SiteTasarimi/Arka uc (Backend)/veriler.db")
cursor = conn.cursor()

# Tüm siteleri al
cursor.execute("SELECT * FROM 'Site Detayları'")
siteler = cursor.fetchall()

print("----- Site Detayları -----")
for site in siteler:
    print(f"Site ID: {site[0]}, Site Adı: {site[1]}")

conn.close()
