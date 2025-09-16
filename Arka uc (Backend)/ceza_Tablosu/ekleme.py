from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route("/ceza_ekle", methods=["POST"])
def ekle_ceza():
    try:
        data = request.get_json()
        calisan_id = data.get("calisan_id")
        calisan_adi = data.get("calisan_adi")
        site_id = data.get("site_id")
        site_adi = data.get("site_adi")
        saat = data.get("saat")
        tarih = data.get("tarih", datetime.now().strftime("%Y-%m-%d"))  # eğer boşsa bugünün tarihi

        conn = sqlite3.connect(r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\ceza_Tablosu\veriler.db")
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
