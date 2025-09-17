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

@app.route('/api/evaluation', methods=['GET'])
def get_all_evaluations():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Retrieve all records from Evaluation table
        cursor.execute('SELECT * FROM Evaluation')
        rows = cursor.fetchall()

        evaluations = []
        for row in rows:
            evaluations.append({
                'id': row['ID'],
                'employee_id': row['Employee_ID'],
                'name': row['Name'],
                'site_id': row['Site_ID'],
                'site': row['Site'],
                'quality_evaluation': row['Quality_Evaluation'],
                'behavior_evaluation': row['Behavior_Evaluation'],
                'work_hours_evaluation': row['Work_Hours_Evaluation']
            })

        conn.close()
        return jsonify(evaluations), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
