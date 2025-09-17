from flask import Flask, request, jsonify
import sqlite3
from config import DATABASE
import traceback

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/loans/update', methods=['PUT'])
def update_loan():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    loan_id = data.get('ID') or data.get('id')  # Accept both
    loan_amount = data.get('Loan') or data.get('loan')

    if not all([loan_id, loan_amount]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update only the Loan amount
        cursor.execute('''
            UPDATE Loans
            SET Loan = ?
            WHERE ID = ?
        ''', (loan_amount, loan_id))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Loan not found'}), 404

        conn.commit()
        conn.close()

        return jsonify({'message': 'Loan updated successfully'}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
