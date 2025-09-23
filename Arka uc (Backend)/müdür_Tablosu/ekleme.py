from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route('/mudur_ekle', methods=['POST'])
def mudur_ekle():
    data = request.get_json()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # JSON bir liste mi kontrol et
        if isinstance(data, list):
            eklenenler = []
            for item in data:
                mudur_adi = item.get("Müdür Adı")
                is_unvani = item.get("İş Unvanı")
                if not mudur_adi or not is_unvani:
                    continue
                cursor.execute("""
                    INSERT INTO Müdürler ("Müdür Adı", "İş Unvanı")
                    VALUES (?, ?)
                """, (mudur_adi, is_unvani))
                eklenenler.append({"Müdür Adı": mudur_adi, "İş Unvanı": is_unvani})
        else:
            mudur_adi = data.get("Müdür Adı")
            is_unvani = data.get("İş Unvanı")
            if not mudur_adi or not is_unvani:
                return jsonify({"error": "Eksik veri!"}), 400
            cursor.execute("""
                INSERT INTO Müdürler ("Müdür Adı", "İş Unvanı")
                VALUES (?, ?)
            """, (mudur_adi, is_unvani))
            eklenenler = [{"Müdür Adı": mudur_adi, "İş Unvanı": is_unvani}]

        conn.commit()
        conn.close()
        return jsonify({"message": "Müdürler eklendi", "eklenenler": eklenenler})

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
