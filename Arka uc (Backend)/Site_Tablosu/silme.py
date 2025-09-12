from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Veritabanı yolu
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# -----------------------
# Site Silme
# -----------------------
@app.route("/site_sil/<int:site_id>", methods=["DELETE"])
def site_sil(site_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM "Site Detayları" WHERE "Site ID" = ?', (site_id,))
        conn.commit()

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"message": f"❌ Site ID {site_id} bulunamadı"}), 404

        conn.close()
        return jsonify({"message": f"✅ Site ID {site_id} başarıyla silindi"}), 200

    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500

# -----------------------
# Sunucu Başlat
# -----------------------
if __name__ == "__main__":
    app.run(port=5008, debug=True)
