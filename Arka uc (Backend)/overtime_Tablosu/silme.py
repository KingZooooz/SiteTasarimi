from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB_PATH = r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\overtime_Tablosu\veriler.db"

@app.route("/overtime_sil/<int:id>", methods=["DELETE"])
def overtime_sil(id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM "Overtime" WHERE "ID"=?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Overtime silindi. ID: {id}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
