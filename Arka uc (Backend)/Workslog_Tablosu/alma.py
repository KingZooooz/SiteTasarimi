from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Satırları dict gibi kullanabilmek için
    return conn

# -----------------------
# Tüm Worklogs Verilerini Listele
# -----------------------
@app.route("/workslog", methods=["GET"])
def workslog_listele():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Worklogs')
        veriler = []
        for row in cursor.fetchall():
            veriler.append({
                "ID": row["ID"],
                "Çalışan_ID": row["Çalışan_ID"],
                "Çalışan_Adi": row["Çalışan_Adi"],
                "Site_ID": row["Site_ID"],
                "Site_Adi": row["Site_Adi"],
                "Durum": row["Durum"],
                "Calisilan_Saatler": row["Calisilan_Saatler"],
                "Tarih": row["Tarih"],
                "Saat": row["Saat"]
            })
        conn.close()
        return jsonify(veriler), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Sunucu Başlat
# -----------------------
if __name__ == "__main__":
    app.run(port=5011, debug=True)

