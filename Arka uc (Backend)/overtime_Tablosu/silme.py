from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route("/overtime_sil/<int:id>", methods=["DELETE"])
def overtime_sil(id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM "Overtime" WHERE "ID"=?', (id,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Overtime silindi. ID: {id}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
