from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route("/mudur_sil/<int:id>", methods=["DELETE"])
def sil_mudur(id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Müdürler WHERE ID = ?", (id,))
        conn.commit()
        conn.close()

        return jsonify({"message": f"✅ Müdür silindi. ID: {id}"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5004)
