from flask import Flask, request, jsonify
import sqlite3
from config import DATABASE  # Make sure this file defines: DATABASE = 'your_database_name.db'
import traceback


app = Flask(__name__)

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
@app.route('/api/rewards_penalties/add', methods=['POST'])
def add_reward_penalty():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    employee_id = data.get('employee_id')
    absence_hours = data.get('absence_hours')
    extra_time = data.get('extra_time')
    reward = data.get('reward')

    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')  # current date

    if not all([employee_id, absence_hours, extra_time, reward]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get primary site ID
        cursor.execute('''
            SELECT site_id FROM Employee_Sites
            WHERE employee_id = ? AND is_primary = 1
        ''', (employee_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Primary site not found for employee'}), 400
        primary_site_id = row['site_id']

        # Insert into Rewards_And_Penalties
        cursor.execute('''
            INSERT INTO Rewards_And_Penalties
            (Employee_ID, Site_ID, Date, "Absence(Hours)", Extra_Time, Reward)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (employee_id, primary_site_id, date, absence_hours, extra_time, reward))

        conn.commit()
        entry_id = cursor.lastrowid
        conn.close()

        return jsonify({'message': 'Reward/Penalty added', 'id': entry_id}), 201

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
