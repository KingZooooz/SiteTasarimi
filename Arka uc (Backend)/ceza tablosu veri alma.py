import sqlite3

# --- Bağlantıyı aç ---
conn = sqlite3.connect("veriler.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

def listele_ceza():
    cursor.execute("SELECT * FROM Ceza")
    rows = cursor.fetchall()

    if not rows:
        print("❌ Ceza tablosu boş.")
        return []

    ceza_list = []
    for row in rows:
        ceza_list.append({
            "ID": row["ID"],
            "Calisan_ID": row["Calisan_ID"],
            "Calisan_Adi": row["Calisan_Adi"],
            "Site_ID": row["Site_ID"],
            "Site_Adi": row["Site_Adi"],
            "Saat": row["Saat"],
            "Tarih": row["Tarih"]
        })
    return ceza_list

# --- Test ---
veriler = listele_ceza()
for v in veriler:
    print(v)

conn.close()
