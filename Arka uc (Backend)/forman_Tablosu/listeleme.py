from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/forman_listele", methods=["GET"])
def forman_listele():
    conn = sqlite3.connect(r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\forman_Tablosu\veriler.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Forman")
    rows = cursor.fetchall()
    conn.close()

    forman_listesi = [dict(row) for row in rows]
    return jsonify(forman_listesi), 200

if __name__ == "__main__":
    app.run(debug=True)
