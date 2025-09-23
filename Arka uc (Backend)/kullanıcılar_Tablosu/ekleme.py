from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Veritabanı yolu dinamik
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route('/kullanici_ekle', methods=['POST'])
def kullanici_ekle():
    data = request.get_json()

    kullanici_adi = data.get("Kullanıcı_Adi")
    kullanici_tipi = data.get("Kullanıcı_tipi")
    baslama_tarihi = data.get("Baslama_Tarihi", datetime.now().strftime("%Y-%m-%d"))
    is_unvani = data.get("İş_Unvanı", None)  # Müdür için gerekli olacak

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Kullanıcı ekleme
        cursor.execute("""
            INSERT INTO Kullanıcılar (Kullanıcı_Adi, Kullanıcı_tipi, Baslama_Tarihi)
            VALUES (?, ?, ?)
        """, (kullanici_adi, kullanici_tipi, baslama_tarihi))

        # Eğer kullanıcı müdür ise, Müdür tablosuna da ekle
        if kullanici_tipi and kullanici_tipi.lower() == "müdür":
            cursor.execute("""
                INSERT INTO Müdürler ("Müdür Adı", "İş Unvanı")
                VALUES (?, ?)
            """, (kullanici_adi, is_unvani if is_unvani else "Müdür"))

        conn.commit()
        conn.close()

        return jsonify({"message": f"Kullanıcı eklendi: {kullanici_adi} ({kullanici_tipi})"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

