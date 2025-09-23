from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu dinamik
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route('/kullanici_guncelle/<int:kullanici_id>', methods=['PUT'])
def kullanici_guncelle(kullanici_id):
    data = request.get_json()

    kullanici_adi = data.get("Kullanıcı_Adi")
    kullanici_tipi = data.get("Kullanıcı_tipi")
    baslama_tarihi = data.get("Baslama_Tarihi")

    try:
        conn = sqlite3.connect(db_path)
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
