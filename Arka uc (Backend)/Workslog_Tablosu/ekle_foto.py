from flask import Flask, jsonify, request
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)

# Veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

# Fotoğraflar için klasör
upload_folder = os.path.join(base_dir, "uploads")
os.makedirs(upload_folder, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# Tüm Çalışanları Worklogs'a Ekle + Fotoğraf
# -----------------------
@app.route("/add_all_worklogs", methods=["POST"])
def add_all_worklogs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Tüm çalışanları al
        cursor.execute('SELECT "Çalışan ID", "Adı", "Site ID" FROM "Çalışan Detayları"')
        calisanlar = cursor.fetchall()
        if not calisanlar:
            conn.close()
            return jsonify({"error": "Çalışan bulunamadı"}), 404

        eklenenler = []
        for calisan in calisanlar:
            calisan_id = calisan["Çalışan ID"]
            adi = calisan["Adı"]
            site_id = calisan["Site ID"]

            # Site adını al
            cursor.execute('SELECT "Site Adı" FROM "Site Detayları" WHERE "Site ID" = ?', (site_id,))
            site = cursor.fetchone()
            if site is None:
                continue
            site_adi = site["Site Adı"]

            # Durum ve çalışılan saatler
            durum = "devamlı"
            calisilan_saatler = 8 if durum == "devamlı" else 0

            # Tarih ve saat
            tarih = datetime.now().strftime("%Y-%m-%d")
            saat = datetime.now().strftime("%H:%M:%S")

            # Fotoğraf yükleme (opsiyonel)
            foto_path = None
            if f"foto_{calisan_id}" in request.files:
                file = request.files[f"foto_{calisan_id}"]
                filename = f"{calisan_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
                file.save(os.path.join(upload_folder, filename))
                foto_path = os.path.join("uploads", filename)

            # Worklogs tablosuna ekle
            cursor.execute("""
                INSERT INTO Worklogs 
                ("Çalışan_ID", "Çalışan_Adi", "Site_ID", "Site_Adi", "Durum", "Calisilan_Saatler", "Tarih", "Saat", "Fotoğraf_Yolu")
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (calisan_id, adi, site_id, site_adi, durum, calisilan_saatler, tarih, saat, foto_path))

            eklenenler.append({
                "Çalışan ID": calisan_id,
                "Adı": adi,
                "Site Adı": site_adi,
                "Site ID": site_id,
                "Durum": durum,
                "Çalışılan Saatler": calisilan_saatler,
                "Tarih": tarih,
                "Saat": saat,
                "Fotoğraf_Yolu": foto_path
            })

        conn.commit()
        conn.close()

        return jsonify({
            "message": "✅ Tüm çalışanların verileri worklogs tablosuna eklendi",
            "eklenenler": eklenenler
        }), 201

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
