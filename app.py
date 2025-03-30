from flask import Flask, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

@app.route('/healthcheck')
def healthcheck():
    return jsonify({"status": "ok", "message": "Server is running"}), 200

if __name__ == '__main__':
    app.run(debug=True)
