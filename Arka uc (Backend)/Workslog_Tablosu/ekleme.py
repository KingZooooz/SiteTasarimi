from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# Tüm Çalışanları Workslog'a Ekle
# -----------------------
@app.route("/add_all_worklogs", methods=["POST"])
def add_all_worklogs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Tüm çalışanları al
        cursor.execute('SELECT "Çalışan ID", "Adı", "Site ID" FROM "Çalışan Detayları"')
        calisanlar = cursor.fetchall()
        if not calisanlar:
            conn.close()
            return jsonify({"error": "Çalışan bulunamadı"}), 404

        eklenenler = []
        for calisan in calisanlar:
            calisan_id = calisan["Çalışan ID"]
            adi = calisan["Adı"]
            site_id = calisan["Site ID"]

            # Site adını al
            cursor.execute('SELECT "Site Adı" FROM "Site Detayları" WHERE "Site ID" = ?', (site_id,))
            site = cursor.fetchone()
            if site is None:
                continue
            site_adi = site["Site Adı"]

            # workslog tablosuna ekle
            cursor.execute("""
                INSERT INTO workslog ("Çalışan ID", "Adı", "Site Adı", "Site ID")
                VALUES (?, ?, ?, ?)
            """, (calisan_id, adi, site_adi, site_id))

            eklenenler.append({"Çalışan ID": calisan_id, "Adı": adi, "Site Adı": site_adi, "Site ID": site_id})

        conn.commit()
        conn.close()

        return jsonify({
            "message": "✅ Tüm çalışanların verileri workslog tablosuna eklendi",
            "eklenenler": eklenenler
        }), 201

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Sunucu Başlat
# -----------------------
if __name__ == "__main__":
    app.run(port=5010, debug=True)
