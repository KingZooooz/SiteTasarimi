from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH =r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\overtime_Tablosu\veriler.db"

@app.route("/overtime_guncelle/<int:id>", methods=["PUT"])
def overtime_guncelle(id):
    data = request.get_json()
    saat = data.get("saat")
    tarih = data.get("tarih")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('UPDATE "Overtime" SET "Saat"=?, "Tarih"=? WHERE "ID"=?', (saat, tarih, id))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Overtime güncellendi. ID: {id}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
