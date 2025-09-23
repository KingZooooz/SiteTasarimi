from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

# Veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/maas_hesapla", methods=["GET"])
def maas_hesapla():
    try:
        calisan_id = request.args.get("calisan_id", type=int)
        ay = request.args.get("ay", type=int)
        yil = request.args.get("yil", type=int)

        if not calisan_id or not ay or not yil:
            return jsonify({"error": "calisan_id, ay ve yil parametreleri gerekli"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Çalışan bilgisi ve temel maaş
        cursor.execute('SELECT "Adı", "Maaş" FROM "Çalışan Detayları" WHERE "Çalışan ID" = ?', (calisan_id,))
        calisan = cursor.fetchone()
        if not calisan:
            conn.close()
            return jsonify({"error": f"Çalışan ID {calisan_id} bulunamadı"}), 404

        calisan_adi = calisan["Adı"]
        maas = calisan["Maaş"]

        # Worklogs'tan toplam çalışma saatleri (Durum = 'devamlı')
        cursor.execute("""
            SELECT SUM(Calisilan_Saatler) as toplam_saat
            FROM Worklogs
            WHERE "Çalışan_ID" = ?
            AND strftime('%m', Tarih) = ?
            AND strftime('%Y', Tarih) = ?
            AND Durum = 'devamlı'
        """, (calisan_id, f"{ay:02d}", str(yil)))
        worklog = cursor.fetchone()
        toplam_calisma_saatleri = worklog["toplam_saat"] or 0

        # Overtime'tan toplam fazla mesai
        cursor.execute("""
            SELECT SUM(Saat) as toplam_fazla_mesai
            FROM Overtime
            WHERE "Çalışan ID" = ?
            AND strftime('%m', Tarih) = ?
            AND strftime('%Y', Tarih) = ?
        """, (calisan_id, f"{ay:02d}", str(yil)))
        overtime = cursor.fetchone()
        toplam_fazla_mesai = float(overtime["toplam_fazla_mesai"] or 0)

        # Ceza toplamı
        cursor.execute("""
            SELECT SUM(Saat) as toplam_ceza
            FROM Ceza
            WHERE "Çalışan ID" = ?
            AND strftime('%m', Tarih) = ?
            AND strftime('%Y', Tarih) = ?
        """, (calisan_id, f"{ay:02d}", str(yil)))
        ceza = cursor.fetchone()
        toplam_ceza = float(ceza["toplam_ceza"] or 0)

        # Toplam maaş: temel maaş + (fazla mesai*örn 1 birim ücret) - ceza
        # Burada 1 birim ücret = maas / 160 varsayalım (aylık 160 saat çalışma)
        birim_ucret = maas / 160
        toplam_maas = maas + (toplam_fazla_mesai * birim_ucret) - (toplam_ceza * birim_ucret)

        conn.close()

        return jsonify({
            "Çalışan ID": calisan_id,
            "Adı": calisan_adi,
            "Maas": maas,
            "Toplam Calisma Saatleri": toplam_calisma_saatleri,
            "Fazla Mesai": toplam_fazla_mesai,
            "Cezalar": toplam_ceza,
            "Ay": ay,
            "Yıl": yil,
            "Toplam Maas": toplam_maas,
            "Tarih": datetime.now().strftime("%Y-%m-%d")
        }), 200

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5020, debug=True)
