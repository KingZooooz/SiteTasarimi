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

@app.route('/api/jobs/delete/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('DELETE FROM Jobs WHERE ID = ?', (job_id,))
        conn.commit()
        rows_deleted = cursor.rowcount
        conn.close()

        if rows_deleted == 0:
            return jsonify({'error': 'Job not found'}), 404

        return jsonify({'message': f'Job with ID {job_id} deleted successfully'}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
