from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# Çalışan Güncelleme
# -----------------------
@app.route("/calisan_guncelle/<int:emp_id>", methods=["PUT"])
def calisan_guncelle(emp_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Eksik JSON verisi"}), 400

    adi = data.get("Adı")
    yas = data.get("Yaş")
    durum = data.get("Durum")
    maas = data.get("Maaş")
    site_id = data.get("Site ID")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Çalışan var mı kontrol et
        cursor.execute('SELECT * FROM "Çalışan Detayları" WHERE rowid = ?', (emp_id,))
        mevcut = cursor.fetchone()
        if not mevcut:
            conn.close()
            return jsonify({"error": f"Çalışan ID {emp_id} bulunamadı."}), 404

        # Güncellenecek alanlar
        fields = []
        values = []

        if adi is not None:
            fields.append('"Adı" = ?')
            values.append(adi)
        if yas is not None:
            fields.append('"Yaş" = ?')
            values.append(yas)
        if durum is not None:
            fields.append('"Durum" = ?')
            values.append(durum)
        if maas is not None:
            fields.append('"Maaş" = ?')
            values.append(maas)
        if site_id is not None:
            fields.append('"Site ID" = ?')
            values.append(site_id)

        if not fields:
            conn.close()
            return jsonify({"error": "Güncellenecek alan yok"}), 400

        query = f'UPDATE "Çalışan Detayları" SET {", ".join(fields)} WHERE rowid = ?'
        values.append(emp_id)

        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return jsonify({"message": f"✅ Çalışan ID {emp_id} başarıyla güncellendi"}), 200

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Sunucu Başlat
# -----------------------
if __name__ == "__main__":
    app.run(port=5002, debug=True)
