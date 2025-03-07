from flask import Flask, jsonify
import sqlite3
import os
import requests
from dotenv import load_dotenv
from flask_cors import CORS

# ✅ Load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)  # ✅ Allow React to call API

ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")


# ✅ Function to connect to database
def get_db_connection():
    db_path = '/Users/kamisama/Desktop/Investment Tracker/investment.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return "<h1>✅ Flask API Running! Use <a href='/api/tables'>/api/tables</a> to get data.</h1>"


# ✅ Ensure API returns table names correctly
@app.route('/api/tables', methods=['GET'])
def get_tables():
    conn = get_db_connection()
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    conn.close()

    table_names = [table["name"] for table in tables if table["name"] != "sqlite_sequence"]

    if not table_names:
        return jsonify({"error": "No tables found"}), 404  # ✅ Return error if no tables

    return jsonify(table_names)

@app.route('/api/bank_accounts', methods=['GET'])
def get_bank_accounts():
    conn = get_db_connection()
    accounts = conn.execute("SELECT * FROM bank_accounts").fetchall()
    conn.close()

    if not accounts:
        return jsonify({"error": "No bank accounts found"}), 404  # ✅ Return an error if no data

    return jsonify([dict(account) for account in accounts])

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    conn = get_db_connection()
    stocks = conn.execute("SELECT * FROM stocks").fetchall()
    conn.close()

    if not stocks:
        return jsonify({"error": "No stocks found"}), 404  # ✅ Return an error if no data

    return jsonify([dict(stock) for stock in stocks])

if __name__ == '__main__':
    print("✅ Flask API is running at http://127.0.0.1:5000/")
    app.run(debug=True)
