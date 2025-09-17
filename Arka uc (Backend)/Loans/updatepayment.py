from flask import Flask, jsonify, request
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

@app.route('/api/loans/updatepayment', methods=['PUT'])
def update_payment():
    """
    Update the amount of a loan payment.
    Expected JSON: { "ID": 1, "Amount": 500 }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Missing JSON data'}), 400

    payment_id = data.get("ID")
    new_amount = data.get("Amount")

    if not all([payment_id, new_amount]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if payment exists
        cursor.execute("SELECT * FROM LoanPayments WHERE ID = ?", (payment_id,))
        payment = cursor.fetchone()
        if not payment:
            return jsonify({'error': 'Payment not found'}), 404

        # Update the amount
        cursor.execute(
            "UPDATE LoanPayments SET Amount = ? WHERE ID = ?",
            (new_amount, payment_id)
        )
        conn.commit()
        conn.close()

        return jsonify({'message': 'Payment updated successfully'}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
