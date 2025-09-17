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

@app.route('/api/evaluation/update', methods=['PUT'])
def update_evaluation():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    evaluation_id = data.get('id')  # ID of the evaluation record to update
    employee_id = data.get('employee_id')
    quality_evaluation = data.get('quality_evaluation')
    behavior_evaluation = data.get('behavior_evaluation')
    work_hours_evaluation = data.get('work_hours_evaluation')

    if not all([evaluation_id, employee_id, quality_evaluation, behavior_evaluation, work_hours_evaluation]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 1. Get employee name from EmployeesTickets
        cursor.execute('SELECT Name FROM EmployeesTickets WHERE id = ?', (employee_id,))
        emp_row = cursor.fetchone()
        if not emp_row:
            return jsonify({'error': 'Employee not found in EmployeesTickets'}), 404
        employee_name = emp_row['Name']

        # 2. Get primary site ID from Employee_Sites
        cursor.execute('''
            SELECT site_id FROM Employee_Sites
            WHERE employee_id = ? AND is_primary = 1
        ''', (employee_id,))
        site_row = cursor.fetchone()
        if not site_row:
            return jsonify({'error': 'Primary site not found for employee'}), 404
        site_id = site_row['site_id']

        # 3. Get site name from Sites table
        cursor.execute('SELECT Site FROM Sites WHERE ID_Site = ?', (site_id,))
        site_name_row = cursor.fetchone()
        if not site_name_row:
            return jsonify({'error': 'Site not found in Sites table'}), 404
        site_name = site_name_row['Site']

        # 4. Update Evaluation record
        cursor.execute('''
            UPDATE Evaluation
            SET Employee_ID = ?, Name = ?, Site_ID = ?, Site = ?,
                Quality_Evaluation = ?, Behavior_Evaluation = ?, Work_Hours_Evaluation = ?
            WHERE ID = ?
        ''', (
            employee_id,
            employee_name,
            site_id,
            site_name,
            quality_evaluation,
            behavior_evaluation,
            work_hours_evaluation,
            evaluation_id
        ))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Evaluation record not found'}), 404

        conn.commit()
        conn.close()

        return jsonify({'message': 'Evaluation updated successfully'}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500