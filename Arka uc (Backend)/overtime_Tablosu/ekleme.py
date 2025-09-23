from flask import Flask, request, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route("/overtime_ekle", methods=["POST"])
def overtime_ekle():
    data = request.get_json()
    calisan_id = data.get("calisan_id")
    site_id = data.get("site_id")
    saat = data.get("saat")
    tarih = data.get("tarih", datetime.now().strftime("%Y-%m-%d"))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Çalışan adı
    cursor.execute('SELECT "Adı" FROM "Çalışan Detayları" WHERE "Çalışan ID"=?', (calisan_id,))
    calisan = cursor.fetchone()
    if not calisan:
        conn.close()
        return jsonify({"error": "Çalışan bulunamadı"}), 400
    calisan_adi = calisan[0]

    # Site adı
    cursor.execute('SELECT "Site Adı" FROM "Site Detayları" WHERE "Site ID"=?', (site_id,))
    site = cursor.fetchone()
    if not site:
        conn.close()
        return jsonify({"error": "Site bulunamadı"}), 400
    site_adi = site[0]

    cursor.execute('INSERT INTO "Overtime" ("Çalışan ID","Çalışan Adı","Site ID","Site Adı","Saat","Tarih") VALUES (?,?,?,?,?,?)',
                   (calisan_id, calisan_adi, site_id, site_adi, saat, tarih))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Overtime eklendi: {calisan_adi} ({site_adi}) - {saat}, {tarih}"}), 200

if __name__ == "__main__":
    app.run(debug=True)


