from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Get the folder where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # So results can be accessed like dictionaries
    return conn


@app.route("/add_employee", methods=["POST"])
def calisan_ekle():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    adi = data.get("Adı")
    yas = data.get("Yaş")
    durum = data.get("Durum")
    maas = data.get("Maaş")
    site_id = data.get("Site ID")

    if not all([adi, yas, durum, maas, site_id]):
        return jsonify({"error": "Eksik veri gönderildi"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO "Çalışan Detayları" ("Adı", "Yaş", "Durum", "Maaş", "Site ID")
            VALUES (?, ?, ?, ?, ?)
        """, (adi, yas, durum, maas, site_id))
        conn.commit()
        conn.close()

        # Return the inserted data as JSON
        return jsonify({
            "Adı": adi,
            "Yaş": yas,
            "Durum": durum,
            "Maaş": maas,
            "Site ID": site_id,
            "message": "✅ Çalışan başarıyla eklendi."
        }), 201

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
