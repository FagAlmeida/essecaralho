from flask import Flask, render_template, request, jsonify
import os
from pymongo import MongoClient

app = Flask(__name__)

# Conexão direta com MongoDB (sem Flask-PyMongo)
client = MongoClient(os.getenv("MONGO_URI", "mongodb+srv://fagalmeida:1234@cluster0.xm9sz.mongodb.net/?retryWrites=true&w=majority"))
db = client.get_database("meu_banco")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login-test', methods=['GET', 'POST'])
def login_test():
    if request.method == 'POST':
        try:
            user = db.usuarios.find_one({"username": request.form.get('username')})
            if user:
                return jsonify({"status": "success", "user": user["username"]})
            return jsonify({"status": "user_not_found"}), 404
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
