from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/kullanici_listele', methods=['GET'])
def kullanici_listele():
    try:
        conn = sqlite3.connect(r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\kullanıcılar_Tablosu\veriler.db")
        conn.row_factory = sqlite3.Row  # kolon isimleriyle erişim için
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Kullanıcılar")
        rows = cursor.fetchall()

        veriler = []
        for row in rows:
            veriler.append({
                "ID": row["ID"],
                "Kullanıcı_Adi": row["Kullanıcı_Adi"],
                "Kullanıcı_tipi": row["Kullanıcı_tipi"],
                "Baslama_Tarihi": row["Baslama_Tarihi"]
            })

        conn.close()
        return jsonify(veriler)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
