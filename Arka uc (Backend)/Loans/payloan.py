from flask import Flask, jsonify, request
import sqlite3
import os
import traceback
import datetime  # keep the module import

app = Flask(__name__)


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/loans/pay', methods=['POST'])
def pay_loan():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    employee_id = data.get('employee_id')
    payment_amount = data.get('payment')

    # Use the correct datetime reference
    date = datetime.datetime.now().strftime('%Y-%m-%d')

    if not all([employee_id, payment_amount]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get the primary site of the employee
        cursor.execute('''
            SELECT site_id FROM employee_sites
            WHERE employee_id = ? AND is_primary = 1
        ''', (employee_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Primary site not found for employee'}), 400

        site_id = row['site_id']

        # Insert payment
        cursor.execute('''
            INSERT INTO LoanPayments (Employee_ID, Site_ID, Date, Amount)
            VALUES (?, ?, ?, ?)
        ''', (employee_id, site_id, date, payment_amount))

        conn.commit()
        conn.close()

        return jsonify({
            'message': 'Payment recorded successfully',
            'site_id': site_id
        }), 201

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
