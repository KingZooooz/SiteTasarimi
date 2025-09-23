from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route("/mudur_guncelle/<int:id>", methods=["PUT"])
def guncelle_mudur(id):
    try:
        data = request.get_json()
        mudur_adi = data.get("Müdür_Adi")
        unvan = data.get("İş_Unvanı")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Müdürler SET "Müdür Adı" = ?, "İş Unvanı" = ? WHERE ID = ?
        """, (mudur_adi, unvan, id))

        conn.commit()
        conn.close()

        return jsonify({"message": f"✅ Müdür güncellendi. ID: {id}"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5003)
