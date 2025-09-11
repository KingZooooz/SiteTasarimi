from flask import Flask, jsonify
import sqlite3
import os

app = Flask(__name__)

# Script'in bulunduğu klasör
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/employees", methods=["GET"])
def calisanlari_listele():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Çalışan Detayları"')
        rows = cursor.fetchall()
        conn.close()

        employees = [dict(row) for row in rows]

        return jsonify({
            "success": True,
            "count": len(employees),
            "employees": employees
        }), 200

    except sqlite3.Error as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5002, debug=True)
