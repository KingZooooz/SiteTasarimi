from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

@app.route("/forman_sil", methods=["DELETE"])
def forman_sil():
    data = request.get_json()
    forman_id = data.get("id")
    if not forman_id:
        return jsonify({"error": "Forman ID gerekli"}), 400

    conn = sqlite3.connect(r"D:\Business woman\SiteTasarimi\Arka uc (Backend)\forman_Tablosu\veriler.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Forman WHERE ID=?", (forman_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"Forman silindi. ID: {forman_id}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
