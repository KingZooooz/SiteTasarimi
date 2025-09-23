from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route("/mudur_listele", methods=["GET"])
def listele_mudur():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Müdürler")
        veriler = cursor.fetchall()
        conn.close()

        mudurler = []
        for v in veriler:
            mudurler.append({"ID": v[0], "Müdür Adı": v[1], "İş Unvanı": v[2]})

        return jsonify(mudurler)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5002)
