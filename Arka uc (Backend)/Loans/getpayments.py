from flask import Flask, jsonify
import sqlite3
from config import DATABASE
import traceback

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/loans/payments', methods=['GET'])
def get_payments():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT lp.ID, lp.Employee_ID, e.Name as Employee_Name, lp.Site_ID, s.Site, lp.Date, lp.Amount
            FROM LoanPayments lp
            JOIN EmployeesTickets e ON lp.Employee_ID = e.id
            JOIN Sites s ON lp.Site_ID = s.ID_Site
        ''')
        payments = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify(payments)  # <-- Must be a list!
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
