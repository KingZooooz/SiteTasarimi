from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Dinamik DB yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/forman_guncelle", methods=["PUT"])
def forman_guncelle():
    data = request.get_json()
    forman_id = data.get("id")
    kullanici_adi = data.get("kullanici_adi")
    site_id = data.get("site_id")
    baslama_tarihi = data.get("baslama_tarihi")

    if not forman_id:
        return jsonify({"error": "Forman ID gerekli"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Eğer site_id verilmişse site adını çek
    site_adi = None
    if site_id:
        cursor.execute("SELECT [Site Adı] FROM [Site Detayları] WHERE [Site ID]=?", (site_id,))
        site = cursor.fetchone()
        if not site:
            conn.close()
            return jsonify({"error": f"Site ID {site_id} bulunamadı"}), 400
        site_adi = site[0]

    # Güncellenecek alanları hazırla
    update_fields = []
    values = []
    if kullanici_adi:
        update_fields.append("Kullanıcı_Adi=?")
        values.append(kullanici_adi)
    if site_id:
        update_fields.append("Site_ID=?")
        values.append(site_id)
        update_fields.append("Site_Adi=?")
        values.append(site_adi)
    if baslama_tarihi:
        update_fields.append("Baslama_Tarihi=?")
        values.append(baslama_tarihi)

    if not update_fields:
        conn.close()
        return jsonify({"error": "Güncellenecek alan yok"}), 400

    # Sorgu çalıştır
    values.append(forman_id)
    cursor.execute(f"UPDATE Forman SET {', '.join(update_fields)} WHERE ID=?", values)
    conn.commit()
    conn.close()

    return jsonify({"message": f"✅ Forman güncellendi. ID: {forman_id}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
