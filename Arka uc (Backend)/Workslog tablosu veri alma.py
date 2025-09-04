import sqlite3

conn = sqlite3.connect("D:/Business woman/SiteTasarimi/Arka uc (Backend)/veriler.db")
cursor = conn.cursor()

# Tüm kayıtları al
cursor.execute("SELECT * FROM workslog")
loglar = cursor.fetchall()

print("----- Workslog -----")
for log in loglar:
    print(f"ID: {log[0]}, Çalışan ID: {log[1]}, Adı: {log[2]}, Site Adı: {log[3]}, Site ID: {log[4]}, Saat: {log[5]}, Tarih: {log[6]}")

conn.close()
