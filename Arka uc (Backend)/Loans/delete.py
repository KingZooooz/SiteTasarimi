from flask import Flask, request, jsonify
import sqlite3
from config import DATABASE
import traceback

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/loans/delete/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the loan exists
        cursor.execute('SELECT * FROM Loans WHERE ID = ?', (loan_id,))
        loan = cursor.fetchone()
        if not loan:
            conn.close()
            return jsonify({'error': f'Loan with ID {loan_id} not found'}), 404

        # Delete the loan
        cursor.execute('DELETE FROM Loans WHERE ID = ?', (loan_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': f'Loan with ID {loan_id} deleted successfully'}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500