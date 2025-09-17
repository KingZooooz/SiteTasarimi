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

@app.route('/api/rewards_penalties', methods=['GET'])
def get_rewards_penalties():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Rewards_And_Penalties')
        rows = cursor.fetchall()
        conn.close()

        results = []
        for row in rows:
            results.append({
                'id': row['ID'],
                'employee_id': row['Employee_ID'],
                'site_id': row['Site_ID'],
                'date': row['Date'],
                'absence_hours': row['Absence(Hours)'],
                'extra_time': row['Extra_Time'],
                'reward': row['Reward']
            })

        return jsonify(results), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
