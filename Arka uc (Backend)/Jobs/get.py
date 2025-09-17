from flask import Flask, jsonify
import sqlite3
from config import DATABASE
import traceback
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # allows dict-like access
    return conn

@app.route('/api/jobs', methods=['GET'])
def get_all_jobs():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Jobs')
        rows = cursor.fetchall()
        conn.close()

        jobs = [dict(row) for row in rows]  # convert sqlite rows to dicts

        return jsonify(jobs), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
