from flask import Flask, jsonify, request
import sqlite3
from datetime import datetime
import os
import pandas as pd  # Excel'e aktarmak için

app = Flask(__name__)

# Veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

# Excel çıktısının kaydedileceği dosya
excel_path = os.path.join(base_dir, "maas_raporu.xlsx")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/maas_hesapla", methods=["GET"])
def maas_hesapla():
    try:
        ay = request.args.get("ay", type=int)
        yil = request.args.get("yil", type=int)

        if not ay or not yil:
            return jsonify({"error": "ay ve yil parametreleri gerekli"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Tüm çalışanları al
        cursor.execute('SELECT "Çalışan ID", "Adı", "Maaş" FROM "Çalışan Detayları"')
        calisanlar = cursor.fetchall()

        if not calisanlar:
            conn.close()
            return jsonify({"error": "Çalışan bulunamadı"}), 404

        sonuc_listesi = []

        for calisan in calisanlar:
            calisan_id = calisan["Çalışan ID"]
            calisan_adi = calisan["Adı"]
            maas = float(calisan["Maaş"])

            # Worklogs'tan toplam çalışma saatleri
            cursor.execute("""
                SELECT SUM(Calisilan_Saatler) as toplam_saat
                FROM Worklogs
                WHERE "Çalışan_ID" = ?
                AND strftime('%m', Tarih) = ?
                AND strftime('%Y', Tarih) = ?
                AND Durum = 'devamlı'
            """, (calisan_id, f"{ay:02d}", str(yil)))
            worklog = cursor.fetchone()
            toplam_calisma_saatleri = float(worklog["toplam_saat"] or 0)

            # Overtime toplamı
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

            # Maaş hesabı (172 saat baz alınarak)
            birim_ucret = maas / 172
            toplam_maas = maas + (toplam_fazla_mesai * birim_ucret) - (toplam_ceza * birim_ucret)

            sonuc_listesi.append({
                "Çalışan ID": calisan_id,
                "Adı": calisan_adi,
                "Maaş": round(maas, 2),
                "Toplam Çalışma Saatleri": round(toplam_calisma_saatleri, 2),
                "Fazla Mesai": round(toplam_fazla_mesai, 2),
                "Cezalar": round(toplam_ceza, 2),
                "Ay": ay,
                "Yıl": yil,
                "Toplam Maaş": round(toplam_maas, 2),
                "Tarih": datetime.now().strftime("%Y-%m-%d")
            })

        conn.close()

        # ✅ Excel'e aktarma
        df = pd.DataFrame(sonuc_listesi)
        df.to_excel(excel_path, index=False)

        return jsonify({
            "message": f"Maaş hesaplama tamamlandı ({len(sonuc_listesi)} çalışan).",
            "excel_dosyasi": excel_path,
            "veriler": sonuc_listesi
        }), 200

    except sqlite3.Error as e:
        return jsonify({"error": f"Veritabanı hatası: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Beklenmeyen hata: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(port=5020, debug=True)


