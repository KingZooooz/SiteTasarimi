from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\overtime_Tablosu\veriler.db"

@app.route("/overtime_listele", methods=["GET"])
def overtime_listele():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM "Overtime"')
    rows = cursor.fetchall()
    conn.close()

    liste = [dict(row) for row in rows]
    return jsonify(liste), 200

if __name__ == "__main__":
    app.run(debug=True)
