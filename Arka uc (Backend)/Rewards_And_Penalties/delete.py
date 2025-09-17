
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


@app.route('/api/rewards_penalties/delete/<int:entry_id>', methods=['DELETE'])
def delete_reward_penalty(entry_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the entry exists
        cursor.execute('SELECT * FROM Rewards_And_Penalties WHERE ID = ?', (entry_id,))
        entry = cursor.fetchone()
        if not entry:
            conn.close()
            return jsonify({'error': f'No reward/penalty entry found with ID {entry_id}'}), 404

        # Delete the entry
        cursor.execute('DELETE FROM Rewards_And_Penalties WHERE ID = ?', (entry_id,))
        conn.commit()
        conn.close()

        return jsonify({'message': f'Reward/Penalty entry with ID {entry_id} deleted successfully'}), 200

    except Exception as e:
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500