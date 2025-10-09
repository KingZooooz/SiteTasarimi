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


@app.route("/add_login", methods=["POST"])
def login_ekle():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    kullanici_adi = data.get("Kullanici_Adi")
    sifre = data.get("Sifre")

    if not kullanici_adi or not sifre:
        return jsonify({"error": "Kullanıcı adı ve şifre gereklidir"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Login ("Kullanici_Adi", "Sifre")
            VALUES (?, ?)
        """, (kullanici_adi, sifre))
        conn.commit()
        conn.close()

        return jsonify({
            "Kullanici_Adi": kullanici_adi,
            "message": "✅ Kullanıcı başarıyla eklendi."
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Bu kullanıcı adı zaten mevcut"}), 400
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
