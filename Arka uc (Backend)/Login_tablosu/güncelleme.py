from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/update_login", methods=["PUT"])
def update_login():
    data = request.get_json()
    kullanici_adi = data.get("Kullanici_Adi")
    yeni_sifre = data.get("Yeni_Sifre")

    if not kullanici_adi or not yeni_sifre:
        return jsonify({"error": "Kullanıcı adı ve yeni şifre gereklidir"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Login
            SET Sifre = ?
            WHERE Kullanici_Adi = ?
        """, (yeni_sifre, kullanici_adi))
        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": f"{kullanici_adi} bulunamadı"}), 404

        conn.close()
        return jsonify({"message": f"Kullanıcı şifresi güncellendi: {kullanici_adi}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5030, debug=True)
