from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

@app.route('/kullanici_ekle', methods=['POST'])
def kullanici_ekle():
    data = request.get_json()

    kullanici_adi = data.get("Kullanıcı_Adi")
    kullanici_tipi = data.get("Kullanıcı_tipi")
    baslama_tarihi = data.get("Baslama_Tarihi", datetime.now().strftime("%Y-%m-%d"))

    try:
        conn = sqlite3.connect(r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\kullanıcılar_Tablosu\veriler.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Kullanıcılar (Kullanıcı_Adi, Kullanıcı_tipi, Baslama_Tarihi)
            VALUES (?, ?, ?)
        """, (kullanici_adi, kullanici_tipi, baslama_tarihi))

        conn.commit()
        conn.close()

        return jsonify({"message": f"Kullanıcı eklendi: {kullanici_adi} ({kullanici_tipi})"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
