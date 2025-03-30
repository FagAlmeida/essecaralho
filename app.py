from flask import Flask, render_template, request, jsonify
import os
from pymongo import MongoClient
from urllib.parse import quote_plus

app = Flask(__name__)

# Configuração robusta do MongoDB
def get_mongo_connection():
    try:
        username = quote_plus(os.getenv('MONGO_USERNAME', 'fagalmeida'))
        password = quote_plus(os.getenv('MONGO_PASSWORD', '1234'))
        cluster = os.getenv('MONGO_CLUSTER', 'cluster0.xm9sz.mongodb.net')
        dbname = os.getenv('MONGO_DBNAME', 'meu_banco')
        
        uri = f"mongodb+srv://{username}:{password}@{cluster}/{dbname}?retryWrites=true&w=majority"
        client = MongoClient(uri, connectTimeoutMS=30000, serverSelectionTimeoutMS=30000)
        client.admin.command('ping')  # Testa a conexão
        return client[dbname]
    except Exception as e:
        print(f"🔥 ERRO DE CONEXÃO: {str(e)}")
        return None

db = get_mongo_connection()

@app.route('/debug')
def debug():
    if not db:
        return "❌ Falha na conexão com MongoDB", 500
    return "✅ Servidor operacional + MongoDB conectado", 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if not db:
            return "Erro no banco de dados", 500
            
        if request.method == 'POST':
            username = request.form.get('username')
            user = db.usuarios.find_one({"username": username})
            
            if not user:
                return "Usuário não encontrado", 404
                
            return f"Bem-vindo {user['username']}", 200
            
        return render_template('login.html')
        
    except Exception as e:
        print(f"🚨 ERRO NO LOGIN: {str(e)}")
        return f"Erro interno: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)
