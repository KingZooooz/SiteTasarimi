from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# Site Ekleme
# -----------------------
@app.route("/site_ekle", methods=["POST"])
def site_ekle():
    data = request.get_json()
    if not data or "Site Adı" not in data:
        return jsonify({"error": "Eksik JSON verisi"}), 400

    site_adi = data["Site Adı"]

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO "Site Detayları" ("Site Adı")
            VALUES (?)
        """, (site_adi,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"✅ Site başarıyla eklendi: {site_adi}"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Sunucu Başlat
# -----------------------
if __name__ == "__main__":
    app.run(port=5005, debug=True)
