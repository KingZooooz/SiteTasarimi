from flask import Flask, request, jsonify
import sqlite3
import os
import traceback

app = Flask(__name__)



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/jobs/update', methods=['PUT'])
def update_job():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Missing JSON data'}), 400

        job_id = data.get('ID')
        job_name = data.get('Job')

        if not job_id or not job_name:
            return jsonify({'error': 'Missing required fields: ID and Job'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE Jobs
            SET Job = ?
            WHERE ID = ?
        ''', (job_name, job_id))
        conn.commit()
        affected = cursor.rowcount
        conn.close()

        if affected == 0:
            return jsonify({'error': 'Job not found'}), 404

        return jsonify({
            'message': 'Job updated successfully',
            'job_id': job_id,
            'job_name': job_name
        }), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
