import sqlite3

# --- Bağlantıyı aç ---
conn = sqlite3.connect("veriler.db")
conn.row_factory = sqlite3.Row  # Satırları sözlük gibi almak için
cursor = conn.cursor()

def listele_formanlar():
    cursor.execute("SELECT * FROM Forman")
    rows = cursor.fetchall()

    if not rows:
        print("❌ Forman tablosu boş.")
        return []

    # Satırları sözlük listesi hâline getir
    forman_list = []
    for row in rows:
        forman_list.append({
            "ID": row["ID"],
            "Kullanıcı_Adi": row["Kullanıcı_Adi"],
            "Site_ID": row["Site_ID"],
            "Site_Adi": row["Site_Adi"],
            "Baslama_Tarihi": row["Baslama_Tarihi"]
        })
    return forman_list

# --- Test ---
veriler = listele_formanlar()
for v in veriler:
    print(v)

conn.close()
