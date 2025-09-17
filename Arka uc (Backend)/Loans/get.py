from flask import Flask, jsonify
import sqlite3
import os
import traceback

app = Flask(__name__)


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")

def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/loans', methods=['GET'])
def get_loans():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                Loans.ID,
                Loans.Employee_ID,
                EmployeesTickets.Name AS Employee_Name,
                Loans.Date,
                Loans.Site_ID,
                Sites.Site AS Site_Name,
                Loans.Loan
            FROM Loans
            LEFT JOIN EmployeesTickets ON Loans.Employee_ID = EmployeesTickets.id
            LEFT JOIN Sites ON Loans.Site_ID = Sites.ID_Site
            ORDER BY Loans.Date DESC
        ''')

        loans = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return jsonify(loans), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500