from flask import Flask, request, jsonify
import sqlite3
import os

app = Flask(__name__)

# Script'in bulunduğu klasör
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# Workslog Silme
# -----------------------
@app.route("/workslog_sil/<int:calisan_id>", methods=["DELETE"])
def workslog_sil(calisan_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Önce var mı kontrol et
        cursor.execute('SELECT * FROM Worklogs WHERE "Çalışan_ID" = ?', (calisan_id,))
        mevcut = cursor.fetchone()

        if not mevcut:
            conn.close()
            return jsonify({"error": f"Çalışan ID {calisan_id} workslog tablosunda bulunamadı."}), 404

        # Silme işlemi
        cursor.execute('DELETE FROM Worklogs WHERE "Çalışan_ID" = ?', (calisan_id,))
        conn.commit()
        conn.close()

        return jsonify({
            "success": True,
            "message": f"✅ Çalışan ID {calisan_id} workslog tablosundan silindi."
        }), 200

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Sunucu Başlat
# -----------------------
if __name__ == "__main__":
    app.run(port=5013, debug=True)
