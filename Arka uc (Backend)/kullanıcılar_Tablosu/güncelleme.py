from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/kullanici_guncelle/<int:kullanici_id>', methods=['PUT'])
def kullanici_guncelle(kullanici_id):
    data = request.get_json()

    kullanici_adi = data.get("Kullanıcı_Adi")
    kullanici_tipi = data.get("Kullanıcı_tipi")
    baslama_tarihi = data.get("Baslama_Tarihi")

    try:
        conn = sqlite3.connect(r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\kullanıcılar_Tablosu\veriler.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Kullanıcılar
            SET Kullanıcı_Adi = ?, Kullanıcı_tipi = ?, Baslama_Tarihi = ?
            WHERE ID = ?
        """, (kullanici_adi, kullanici_tipi, baslama_tarihi, kullanici_id))

        conn.commit()
        conn.close()

        return jsonify({"message": f"Kullanıcı güncellendi. ID: {kullanici_id}"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
