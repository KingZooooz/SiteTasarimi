from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route("/overtime_listele", methods=["GET"])
def overtime_listele():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM "Overtime"')
    rows = cursor.fetchall()
    conn.close()

    liste = [dict(row) for row in rows]
    return jsonify(liste), 200

if __name__ == "__main__":
    app.run(debug=True)
