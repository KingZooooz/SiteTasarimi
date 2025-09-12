from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Satırları dict gibi kullanabilmek için
    return conn

# -----------------------
# Tüm Workslog Verilerini Listele
# -----------------------
@app.route("/workslog", methods=["GET"])
def workslog_listele():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM workslog')
        veriler = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(veriler), 200
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Sunucu Başlat
# -----------------------
if __name__ == "__main__":
    app.run(port=5011, debug=True)
