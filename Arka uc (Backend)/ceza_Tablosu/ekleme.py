from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    return conn

@app.route("/ceza_ekle", methods=["POST"])
def ekle_ceza():
    try:
        data = request.get_json()
        calisan_id = data.get("calisan_id")
        calisan_adi = data.get("calisan_adi")
        site_id = data.get("site_id")
        site_adi = data.get("site_adi")
        saat = data.get("saat")
        tarih = data.get("tarih", datetime.now().strftime("%Y-%m-%d"))  # boşsa bugünün tarihi

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Ceza ("Çalışan ID", "Çalışan Adı", "Site ID", "Site Adı", "Saat", "Tarih")
            VALUES (?, ?, ?, ?, ?, ?)
        """, (calisan_id, calisan_adi, site_id, site_adi, saat, tarih))

        conn.commit()
        conn.close()

        return jsonify({
            "message": "✅ Ceza eklendi.",
            "calisan_id": calisan_id,
            "calisan_adi": calisan_adi,
            "site_id": site_id,
            "site_adi": site_adi,
            "saat": saat,
            "tarih": tarih
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
