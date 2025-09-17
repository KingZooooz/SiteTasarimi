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


@app.route('/api/evaluation/<int:employee_id>', methods=['GET'])
def get_evaluation_by_employee(employee_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM Evaluation WHERE Employee_ID = ?', (employee_id,))
        rows = cursor.fetchall()

        if not rows:
            return jsonify({'message': 'No evaluations found for this employee'}), 404

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
