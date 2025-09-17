from flask import Flask, request, jsonify
import sqlite3
from config import DATABASE
import traceback
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/loans/add', methods=['POST'])
def add_loan():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    employee_id = data.get('employee_id')
    loan_amount = data.get('loan')

    # Use current date (yyyy-mm-dd)
    date = datetime.now().strftime('%Y-%m-%d')

    # Validate required fields
    if not all([employee_id, loan_amount]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get the primary site ID for the employee
        cursor.execute('''
            SELECT site_id FROM Employee_Sites
            WHERE employee_id = ? AND is_primary = 1
        ''', (employee_id,))
        row = cursor.fetchone()

        if not row:
            return jsonify({'error': 'Primary site not found for employee'}), 400

        site_id = row['site_id']

        # Insert loan record into the Loans table
        cursor.execute('''
            INSERT INTO Loans
            (Employee_ID, Date, Site_ID, Loan)
            VALUES (?, ?, ?, ?)
        ''', (employee_id, date, site_id, loan_amount))

        conn.commit()
        loan_id = cursor.lastrowid
        conn.close()

        return jsonify({'message': 'Loan added successfully', 'loan_id': loan_id}), 201

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
