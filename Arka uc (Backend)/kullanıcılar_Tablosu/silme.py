from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu dinamik
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

# --- Kullanıcı Silme ---
@app.route("/kullanici_sil/<int:kullanici_id>", methods=["DELETE"])
def kullanici_sil(kullanici_id):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Silmeden önce kullanıcı var mı kontrol et
        cursor.execute("SELECT * FROM Kullanıcılar WHERE ID = ?", (kullanici_id,))
        kullanici = cursor.fetchone()
        if not kullanici:
            conn.close()
            return jsonify({"error": f"Kullanıcı ID {kullanici_id} bulunamadı."}), 404

        # Kullanıcıyı sil
        cursor.execute("DELETE FROM Kullanıcılar WHERE ID = ?", (kullanici_id,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Kullanıcı silindi. ID: {kullanici_id}"}), 200

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True, port=5000)


