from flask import Flask, request, jsonify
import sqlite3
import traceback
from datetime import datetime
import os

app = Flask(__name__)  # This is fine **only if you run this file directly**

# Get the folder where this script is located
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/absence/add', methods=['POST'])
def add_absence():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    employee_id = data.get('employee_id')
    hours = data.get('hours')
    date = datetime.now().strftime('%Y-%m-%d')

    if not all([employee_id, hours]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT site_id FROM Employee_Sites
            WHERE employee_id = ? AND is_primary = 1
        ''', (employee_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Primary site not found for employee'}), 400
        primary_site_id = row['site_id']

        cursor.execute('''
            INSERT INTO absence (Employee_ID, Site_ID, Date, Hours)
            VALUES (?, ?, ?, ?)
        ''', (employee_id, primary_site_id, date, hours))
        conn.commit()
        log_id = cursor.lastrowid
        conn.close()

        return jsonify({'message': 'absence added', 'log_id': log_id}), 201

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
