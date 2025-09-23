from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu dinamik
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route('/mudur_degerlendirme_guncelle/<int:id>', methods=['PUT'])
def mudur_degerlendirme_guncelle(id):
    data = request.get_json()
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Değerlendirme puanlarını al
        kalite = int(data.get("Kalite_Degerlendirmesi"))
        davranis = int(data.get("Davranis_Degerlendirmesi"))
        calisma = int(data.get("Calisma_Saatleri_Degerlendirmesi"))
        memnuniyet = int(data.get("Calisan_Memnuniyeti_Degerlendirmesi"))
        aylik = int(data.get("Aylik_Hedefler_Degerlendirmesi"))
        proje = int(data.get("Proje_Yontemi_Degerlendirmesi"))

        # 1-3 arası kontrol
        for val in [kalite, davranis, calisma, memnuniyet, aylik, proje]:
            if val < 1 or val > 3:
                conn.close()
                return jsonify({"error": "Tüm değerlendirmeler 1-3 arası olmalıdır"}), 400

        # Son değerlendirme hesapla
        son_degerlendirme = round(
            (kalite + davranis + calisma + memnuniyet + aylik + proje) / 6, 2
        )

        # Güncelleme
        cursor.execute("""
            UPDATE Mudur_Degerlendirme
            SET Kalite_Degerlendirmesi=?, Davranis_Degerlendirmesi=?, Calisma_Saatleri_Degerlendirmesi=?,
                Calisan_Memnuniyeti_Degerlendirmesi=?, Aylik_Hedefler_Degerlendirmesi=?, Proje_Yontemi_Degerlendirmesi=?,
                Son_Degerlendirme=?
            WHERE ID=?
        """, (kalite, davranis, calisma, memnuniyet, aylik, proje, son_degerlendirme, id))

        conn.commit()
        conn.close()

        return jsonify({"message": f"Müdür değerlendirmesi güncellendi. ID: {id}", "Son_Degerlendirme": son_degerlendirme})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
