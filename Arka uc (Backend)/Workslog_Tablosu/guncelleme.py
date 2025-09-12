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
# Workslog Güncelleme (SADECE VAR OLAN KAYDI)
# -----------------------
@app.route("/workslog_guncelle/<int:calisan_id>", methods=["PUT"])
def workslog_guncelle(calisan_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Eksik JSON verisi"}), 400

    adi = data.get("Adı")
    site_adi = data.get("Site Adı")
    site_id = data.get("Site ID")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Workslog kaydı var mı kontrol et
        cursor.execute('SELECT * FROM workslog WHERE "Çalışan ID" = ?', (calisan_id,))
        mevcut = cursor.fetchone()
        if not mevcut:
            conn.close()
            return jsonify({"error": f"Çalışan ID {calisan_id} bulunamadı"}), 404

        # Güncellenecek alanları hazırla
        fields = []
        values = []

        if adi is not None:
            fields.append('"Adı" = ?')
            values.append(adi)
        if site_adi is not None:
            fields.append('"Site Adı" = ?')
            values.append(site_adi)
        if site_id is not None:
            fields.append('"Site ID" = ?')
            values.append(site_id)

        if not fields:
            conn.close()
            return jsonify({"error": "Güncellenecek alan yok"}), 400

        query = f'UPDATE workslog SET {", ".join(fields)} WHERE "Çalışan ID" = ?'
        values.append(calisan_id)

        cursor.execute(query, values)
        conn.commit()
        conn.close()

        return jsonify({
            "message": f"✅ Çalışan ID {calisan_id} workslog tablosunda güncellendi"
        }), 200

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Sunucu Başlat
# -----------------------
if __name__ == "__main__":
    app.run(port=5012, debug=True)
