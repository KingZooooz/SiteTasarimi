from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route("/forman_ekle", methods=["POST"])
def forman_ekle():
    data = request.get_json()
    kullanici_adi = data.get("kullanici_adi")
    site_id = data.get("site_id")
    baslama_tarihi = data.get("baslama_tarihi", datetime.now().strftime("%Y-%m-%d"))

    if not kullanici_adi or not site_id:
        return jsonify({"error": "kullanici_adi ve site_id gerekli"}), 400

    conn = sqlite3.connect(r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\forman_Tablosu\veriler.db")
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
    return jsonify({"message": f"Forman eklendi: {kullanici_adi} ({site_adi})"}), 200

if __name__ == "__main__":
    app.run(debug=True)
