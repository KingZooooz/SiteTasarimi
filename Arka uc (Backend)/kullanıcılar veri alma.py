import sqlite3

# --- Bağlantıyı aç ---
conn = sqlite3.connect("veriler.db")
conn.row_factory = sqlite3.Row  # Satırları sözlük gibi almak için
cursor = conn.cursor()

def listele_kullanicilar():
    cursor.execute("SELECT * FROM Kullanıcılar")
    rows = cursor.fetchall()

    if not rows:
        print("❌ Kullanıcılar tablosu boş.")
        return []

    # Satırları sözlük listesi hâline getir
    kullanici_list = []
    for row in rows:
        kullanici_list.append({
            "ID": row["ID"],
            "Kullanıcı_Adi": row["Kullanıcı_Adi"],
            "Kullanıcı_tipi": row["Kullanıcı_tipi"],
            "Baslama_Tarihi": row["Baslama_Tarihi"]
        })
    return kullanici_list

# --- Test ---
veriler = listele_kullanicilar()
for v in veriler:
    print(v)

conn.close()
