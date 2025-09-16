import sqlite3

def listele_overtime():
    conn = sqlite3.connect("veriler.db")
    conn.row_factory = sqlite3.Row  # Böylece sütun isimleri ile erişebiliriz
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM "Overtime"')
    satirlar = cursor.fetchall()

    sonuc = []
    for row in satirlar:
        sonuc.append({
            "Çalışan ID": row["Çalışan ID"],
            "Çalışan Adı": row["Çalışan Adı"],
            "Site ID": row["Site ID"],
            "Site Adı": row["Site Adı"],
            "Saat": row["Saat"],
            "Tarih": row["Tarih"]
        })

    conn.close()
    return sonuc

# ---- Test ----
veriler = listele_overtime()
for v in veriler:
    print(v)

