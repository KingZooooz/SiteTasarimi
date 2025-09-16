from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/forman_guncelle", methods=["PUT"])
def forman_guncelle():
    data = request.get_json()
    forman_id = data.get("id")
    kullanici_adi = data.get("kullanici_adi")
    site_id = data.get("site_id")
    baslama_tarihi = data.get("baslama_tarihi")

    if not forman_id:
        return jsonify({"error": "Forman ID gerekli"}), 400

    conn = sqlite3.connect(r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\forman_Tablosu\veriler.db")
    cursor = conn.cursor()

    # Eğer site_id verilmişse site adını çek
    if site_id:
        cursor.execute("SELECT [Site Adı] FROM [Site Detayları] WHERE [Site ID]=?", (site_id,))
        site = cursor.fetchone()
        if not site:
            conn.close()
            return jsonify({"error": f"Site ID {site_id} bulunamadı"}), 400
        site_adi = site[0]
    else:
        site_adi = None

    # Update sorgusu
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

    values.append(forman_id)
    cursor.execute(f"UPDATE Forman SET {', '.join(update_fields)} WHERE ID=?", values)
    conn.commit()
    conn.close()
    return jsonify({"message": f"Forman güncellendi. ID: {forman_id}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
