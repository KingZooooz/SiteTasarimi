from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu dinamik
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route('/kullanici_listele', methods=['GET'])
def kullanici_listele():
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # kolon isimleriyle erişim için
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Kullanıcılar")
        rows = cursor.fetchall()

        veriler = []
        for row in rows:
            veriler.append({
                "ID": row["ID"],
                "Kullanıcı_Adi": row["Kullanıcı_Adi"],
                "Kullanıcı_tipi": row["Kullanıcı_tipi"],
                "Baslama_Tarihi": row["Baslama_Tarihi"]
            })

        conn.close()
        return jsonify(veriler)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

