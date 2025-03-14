from flask import Flask, jsonify
import sqlite3
import os
from dotenv import load_dotenv
from flask_cors import CORS

# ✅ Load environment variables
load_dotenv()

app = Flask(__name__)

# ✅ Ensure CORS is configured properly
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

# ✅ Function to connect to the database
def get_db_connection():
    db_path = './investment.db'  # Make sure this path is correct
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return "<h1>✅ Flask API Running! Use <a href='/api/bank_accounts'>/api/bank_accounts</a> to get data.</h1>"

@app.route('/api/bank_accounts', methods=['GET'])
def get_bank_accounts():
    conn = get_db_connection()
    accounts = conn.execute("SELECT * FROM bank_account").fetchall()
    conn.close()

    if not accounts:
        return jsonify({"error": "No bank accounts found"}), 404

    return jsonify([dict(account) for account in accounts])

@app.route('/api/bonds', methods=['GET'])
def get_bonds():
    conn = get_db_connection()
    bonds = conn.execute("SELECT * FROM bond").fetchall()
    conn.close()

    if not bonds:
        return jsonify({"error": "No bonds found"}), 404

    return jsonify([dict(bond) for bond in bonds])

if __name__ == '__main__':
    print("✅ Flask API is running at http://127.0.0.1:5000/")
    app.run(debug=True, host='0.0.0.0', port=5000)
