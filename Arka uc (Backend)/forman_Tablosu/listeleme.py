from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu dinamik
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route("/forman_listele", methods=["GET"])
def forman_listele():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Forman")
    rows = cursor.fetchall()
    conn.close()

    forman_listesi = [dict(row) for row in rows]
    return jsonify(forman_listesi), 200

if __name__ == "__main__":
    app.run(debug=True)
