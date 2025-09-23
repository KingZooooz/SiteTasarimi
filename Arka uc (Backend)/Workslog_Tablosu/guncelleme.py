from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# Workslog Güncelleme (Sadece Var Olan Kaydı)
# -----------------------
@app.route("/workslog_guncelle/<int:calisan_id>", methods=["PUT"])
def workslog_guncelle(calisan_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Eksik JSON verisi"}), 400

    adi = data.get("Çalışan_Adi")
    site_adi = data.get("Site_Adi")
    site_id = data.get("Site_ID")
    durum = data.get("Durum")
    calisilan_saatler = data.get("Calisilan_Saatler")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Workslog kaydı var mı kontrol et
        cursor.execute('SELECT * FROM Worklogs WHERE "Çalışan_ID" = ?', (calisan_id,))
        mevcut = cursor.fetchone()
        if not mevcut:
            conn.close()
            return jsonify({"error": f"Çalışan ID {calisan_id} bulunamadı"}), 404

        # Güncellenecek alanları hazırla
        fields = []
        values = []

        if adi is not None:
            fields.append('"Çalışan_Adi" = ?')
            values.append(adi)
        if site_adi is not None:
            fields.append('"Site_Adi" = ?')
            values.append(site_adi)
        if site_id is not None:
            fields.append('"Site_ID" = ?')
            values.append(site_id)
        if durum is not None:
            fields.append('"Durum" = ?')
            values.append(durum)
        if calisilan_saatler is not None:
            fields.append('"Calisilan_Saatler" = ?')
            values.append(calisilan_saatler)

        if not fields:
            conn.close()
            return jsonify({"error": "Güncellenecek alan yok"}), 400

        query = f'UPDATE Worklogs SET {", ".join(fields)} WHERE "Çalışan_ID" = ?'
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

