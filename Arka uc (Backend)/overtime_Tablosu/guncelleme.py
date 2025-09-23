from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route("/overtime_guncelle/<int:id>", methods=["PUT"])
def overtime_guncelle(id):
    data = request.get_json()
    saat = data.get("saat")
    tarih = data.get("tarih")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('UPDATE "Overtime" SET "Saat"=?, "Tarih"=? WHERE "ID"=?', (saat, tarih, id))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Overtime güncellendi. ID: {id}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
