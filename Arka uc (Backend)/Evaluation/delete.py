from flask import Flask, request, jsonify
import sqlite3
import traceback
import os

app = Flask(__name__)

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(base_dir, "veriler.db")


# Connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/evaluation/delete/<int:evaluation_id>', methods=['DELETE'])
def delete_evaluation(evaluation_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the evaluation exists
        cursor.execute('SELECT * FROM Evaluation WHERE ID = ?', (evaluation_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return jsonify({'error': f'No evaluation found with ID {evaluation_id}'}), 404

        # Delete the evaluation record
        cursor.execute('DELETE FROM Evaluation WHERE ID = ?', (evaluation_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': f'Evaluation with ID {evaluation_id} deleted successfully'}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500