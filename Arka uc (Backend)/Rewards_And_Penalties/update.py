from flask import Flask, request, jsonify
import sqlite3
import os
import traceback


app = Flask(__name__)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/rewards_penalties/update', methods=['PUT'])
def update_reward_penalty():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    entry_id = data.get('id')
    employee_id = data.get('employee_id')
    absence_hours = data.get('absence_hours')
    extra_time = data.get('extra_time')
    reward = data.get('reward')

    from datetime import datetime
    date = datetime.now().strftime('%Y-%m-%d')  # current date

    if not all([entry_id, employee_id, absence_hours, extra_time, reward]):
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

        # Update the record
        cursor.execute('''
            UPDATE Rewards_And_Penalties
            SET Employee_ID = ?,
                Site_ID = ?,
                Date = ?,
                "Absence(Hours)" = ?,
                Extra_Time = ?,
                Reward = ?
            WHERE ID = ?
        ''', (employee_id, primary_site_id, date, absence_hours, extra_time, reward, entry_id))

        if cursor.rowcount == 0:
            return jsonify({'error': 'No entry found with the provided ID'}), 404

        conn.commit()
        conn.close()

        return jsonify({'message': 'Reward/Penalty updated successfully', 'id': entry_id}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
