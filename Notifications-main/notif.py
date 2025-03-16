from flask import Flask, jsonify
import sqlite3
import random

app = Flask(__name__)

# Function to fetch a random quote
def get_random_quote():
    conn = sqlite3.connect('healthquote.db')
    cursor = conn.cursor()

    cursor.execute("SELECT text FROM quotes ORDER BY RANDOM() LIMIT 1")
    quote = cursor.fetchone()[0]

    conn.close()
    return quote

# Flask route for serving random quotes
@app.route('/get_random_quote')
def get_quote():
    return jsonify({"quote": get_random_quote()})

if __name__ == '__main__':
    app.run(debug=True)