from flask import Flask, request, jsonify
import sqlite3
from config import DATABASE
import traceback
from datetime import datetime

app = Flask(__name__)  # This is fine **only if you run this file directly**

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/absence/delete/<int:log_id>', methods=['DELETE'])
def delete_absence(log_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the absence entry exists
        cursor.execute('SELECT * FROM absence WHERE id = ?', (log_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return jsonify({'error': f'Absence with ID {log_id} not found'}), 404

        # Delete the absence entry
        cursor.execute('DELETE FROM absence WHERE id = ?', (log_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': f'Absence with ID {log_id} deleted successfully'}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
