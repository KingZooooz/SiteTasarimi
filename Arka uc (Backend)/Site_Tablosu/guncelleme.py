from flask import Flask, request, jsonify
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
# Site Güncelleme
# -----------------------
@app.route("/site_guncelle/<int:site_id>", methods=["PUT"])
def site_guncelle(site_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Eksik JSON verisi"}), 400

    site_adi = data.get("Site Adı")
    if not site_adi:
        return jsonify({"error": "Güncellenecek 'Site Adı' verilmedi"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Site var mı kontrol et
        cursor.execute('SELECT * FROM "Site Detayları" WHERE "Site ID" = ?', (site_id,))
        mevcut = cursor.fetchone()
        if not mevcut:
            conn.close()
            return jsonify({"error": f"Site ID {site_id} bulunamadı"}), 404

        # Güncelle
        cursor.execute('UPDATE "Site Detayları" SET "Site Adı" = ? WHERE "Site ID" = ?', (site_adi, site_id))
        conn.commit()
        conn.close()

        return jsonify({"message": f"✅ Site ID {site_id} başarıyla güncellendi"}), 200

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Sunucu Başlat
# -----------------------
if __name__ == "__main__":
    app.run(port=5007, debug=True)
