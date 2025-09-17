from flask import Flask, request, jsonify
import sqlite3
import os
import traceback
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/jobs/add', methods=['POST'])
def add_job():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing JSON data'}), 400

        job_name = data.get('Job')
        if not job_name:
            return jsonify({'error': 'Missing required field: Job'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert new job
        cursor.execute('INSERT INTO Jobs (Job) VALUES (?)', (job_name,))
        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return jsonify({
            'message': 'Job added successfully',
            'job_id': new_id,
            'job_name': job_name
        }), 201

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
