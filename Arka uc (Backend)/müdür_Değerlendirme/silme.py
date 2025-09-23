from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Dinamik veritabanı yolu
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

@app.route('/mudur_degerlendirme_sil/<int:id>', methods=['DELETE'])
def mudur_degerlendirme_sil(id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM Mudur_Degerlendirme WHERE ID=?", (id,))
        conn.commit()
        conn.close()

        return jsonify({"message": f"Müdür değerlendirmesi silindi. ID: {id}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
