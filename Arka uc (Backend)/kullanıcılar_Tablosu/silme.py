from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# --- Kullanıcı Silme ---
@app.route("/kullanici_sil/<int:kullanici_id>", methods=["DELETE"])
def kullanici_sil(kullanici_id):

    conn = sqlite3.connect(r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\kullanıcılar_Tablosu\veriler.db")
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

if __name__ == "__main__":
    app.run(debug=True, port=5000)

