from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Dinamik DB yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Dict gibi erişim kolaylığı
    return conn

@app.route("/forman_ekle", methods=["POST"])
def forman_ekle():
    data = request.get_json()
    kullanici_adi = data.get("kullanici_adi")
    site_id = data.get("site_id")
    baslama_tarihi = data.get("baslama_tarihi", datetime.now().strftime("%Y-%m-%d"))

    if not kullanici_adi or not site_id:
        return jsonify({"error": "kullanici_adi ve site_id gerekli"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Site adını çek
    cursor.execute("SELECT [Site Adı] FROM [Site Detayları] WHERE [Site ID]=?", (site_id,))
    site = cursor.fetchone()
    if not site:
        conn.close()
        return jsonify({"error": f"Site ID {site_id} bulunamadı"}), 400
    site_adi = site[0]

    cursor.execute("""
        INSERT INTO Forman (Kullanıcı_Adi, Site_ID, Site_Adi, Baslama_Tarihi)
        VALUES (?, ?, ?, ?)
    """, (kullanici_adi, site_id, site_adi, baslama_tarihi))

    conn.commit()
    conn.close()
    return jsonify({"message": f"✅ Forman eklendi: {kullanici_adi} ({site_adi})"}), 200

if __name__ == "__main__":
    app.run(debug=True)
