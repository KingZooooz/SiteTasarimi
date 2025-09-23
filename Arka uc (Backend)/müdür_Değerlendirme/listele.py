from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route('/mudur_degerlendirme_listele', methods=['GET'])
def mudur_degerlendirme_listele():
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Mudur_Degerlendirme")
        rows = cursor.fetchall()

        degerlendirmeler = [dict(row) for row in rows]
        conn.close()

        return jsonify(degerlendirmeler)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
