from flask import Flask, request, jsonify
import sqlite3
from config import DATABASE  # Ensure this has: DATABASE = 'your_database_name.db'
import traceback
from datetime import datetime

app = Flask(__name__)

# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/evaluation/add', methods=['POST'])
def add_evaluation():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    employee_id = data.get('employee_id')
    quality_evaluation = data.get('quality_evaluation')
    behavior_evaluation = data.get('behavior_evaluation')
    work_hours_evaluation = data.get('work_hours_evaluation')
    notes = data.get('notes', '')  # Default to empty string if not provided

    if not all([employee_id, quality_evaluation, behavior_evaluation, work_hours_evaluation]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Today's date
    today = datetime.today().strftime('%Y-%m-%d')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if employee already has any evaluation ever
        cursor.execute('''
            SELECT ID FROM Evaluation
            WHERE Employee_ID = ?
        ''', (employee_id,))
        existing_eval = cursor.fetchone()
        if existing_eval:
            return jsonify({'error': 'Employee already has an evaluation, cannot add another'}), 400

        # Get employee name
        cursor.execute('SELECT Name FROM EmployeesTickets WHERE id = ?', (employee_id,))
        emp_row = cursor.fetchone()
        if not emp_row:
            return jsonify({'error': 'Employee not found in EmployeesTickets'}), 404
        employee_name = emp_row['Name']

        # Get primary site ID
        cursor.execute('''
            SELECT site_id FROM Employee_Sites
            WHERE employee_id = ? AND is_primary = 1
        ''', (employee_id,))
        site_row = cursor.fetchone()
        if not site_row:
            return jsonify({'error': 'Primary site not found for employee'}), 404
        site_id = site_row['site_id']

        # Get site name
        cursor.execute('SELECT Site FROM Sites WHERE ID_Site = ?', (site_id,))
        site_name_row = cursor.fetchone()
        if not site_name_row:
            return jsonify({'error': 'Site not found in Sites table'}), 404
        site_name = site_name_row['Site']

        # Insert evaluation
        cursor.execute('''
            INSERT INTO Evaluation
            (Employee_ID, Name, Site_ID, Site, Quality_Evaluation, Behavior_Evaluation, Work_Hours_Evaluation, Date, Notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            employee_id,
            employee_name,
            site_id,
            site_name,
            quality_evaluation,
            behavior_evaluation,
            work_hours_evaluation,
            today,
            notes
        ))

        conn.commit()
        evaluation_id = cursor.lastrowid
        conn.close()

        return jsonify({'message': 'Evaluation added successfully', 'id': evaluation_id}), 201

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
