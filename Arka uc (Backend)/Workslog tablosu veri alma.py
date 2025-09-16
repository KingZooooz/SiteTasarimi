import sqlite3

# --- Bağlantı aç ---
conn = sqlite3.connect("veriler.db")
conn.row_factory = sqlite3.Row  # Satırları sözlük gibi alabilmek için
cursor = conn.cursor()

def listele_worklogs():
    cursor.execute("SELECT * FROM Worklogs")
    rows = cursor.fetchall()

    if not rows:
        print("❌ Hata: Worklogs tablosu boş.")
        return []

    # Satırları sözlük listesi hâline getir
    worklogs_list = []
    for row in rows:
        worklogs_list.append({
            "ID": row["ID"],
            "Çalışan_ID": row["Çalışan_ID"],
            "Çalışan_Adi": row["Çalışan_Adi"],
            "Site_ID": row["Site_ID"],
            "Site_Adi": row["Site_Adi"],
            "Saat": row["Saat"],
            "Tarih": row["Tarih"]
        })
    return worklogs_list

# --- Test ---
veriler = listele_worklogs()
for v in veriler:
    print(v)

conn.close()

