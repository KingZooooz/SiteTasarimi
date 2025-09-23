from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu dinamik
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route('/mudur_degerlendirme_ekle', methods=['POST'])
def mudur_degerlendirme_ekle():
    data = request.get_json()

    mudur_id = data.get("Mudur_ID")
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Müdür adını çek
        cursor.execute("SELECT [Müdür Adı] FROM Müdürler WHERE ID = ?", (mudur_id,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            return jsonify({"error": f"Müdür ID {mudur_id} bulunamadı"}), 400
        mudur_adi = result[0]

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

        # Son değerlendirme hesapla (ortalama)
        son_degerlendirme = round(
            (kalite + davranis + calisma + memnuniyet + aylik + proje) / 6, 2
        )

        # Veritabanına ekle
        cursor.execute("""
            INSERT INTO Mudur_Degerlendirme 
            (Mudur_ID, Mudur_Adi, Kalite_Degerlendirmesi, Davranis_Degerlendirmesi, 
             Calisma_Saatleri_Degerlendirmesi, Calisan_Memnuniyeti_Degerlendirmesi,
             Aylik_Hedefler_Degerlendirmesi, Proje_Yontemi_Degerlendirmesi, Son_Degerlendirme)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (mudur_id, mudur_adi, kalite, davranis, calisma, memnuniyet, aylik, proje, son_degerlendirme))

        conn.commit()
        conn.close()
        return jsonify({"message": f"Müdür değerlendirmesi eklendi: {mudur_adi}", "Son_Degerlendirme": son_degerlendirme})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
