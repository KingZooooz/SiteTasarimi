from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Satırları dict gibi kullanabilmek için
    return conn

# -----------------------
# Tüm Siteleri Listele
# -----------------------
@app.route("/siteler", methods=["GET"])
def site_listele():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Site Detayları"')
        siteler = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(siteler), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Sunucu Başlat
# -----------------------
if __name__ == "__main__":
    app.run(port=5006, debug=True)
