from flask import Flask, render_template, request, redirect, url_for
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash  # Para hashing de senha

app = Flask(__name__)

# Configuração do MongoDB
app.config["MONGO_URI"] = "mongodb+srv://fagalmeida:1234@cluster0.xm9sz.mongodb.net/meu_banco?retryWrites=true&w=majority"

mongo = PyMongo(app)

# Função para garantir que a coleção 'usuarios' exista
def create_collections():
    # Verifique se a coleção 'usuarios' existe, senão, cria
    if 'usuarios' not in mongo.db.list_collection_names():
        mongo.db.create_collection('usuarios')

# Página inicial
@app.route('/')
def home():
    return render_template('home.html')

# Página inicial (página de "INÍCIO")
@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            # Verifica no banco de dados
            user = mongo.db.usuarios.find_one({'username': username})
            if user and check_password_hash(user['password'], password):  # Verifica o hash da senha
                return redirect(url_for('inicio'))  # Redireciona para a página inicial após login
            else:
                return "Usuário ou senha inválidos", 401
        except Exception as e:
            return f"Erro ao acessar o banco de dados: {e}", 500

    return render_template('login.html')

# Página de registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Verifica se as senhas coincidem
        if password != confirm_password:
            return "As senhas não coincidem. Tente novamente.", 400
        
        try:
            # Verifica se o usuário já existe
            if mongo.db.usuarios.find_one({'username': username}):
                return "Usuário já existe. Tente outro nome.", 400

            # Gera o hash da senha com o método 'pbkdf2:sha256'
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

            # Insere o novo usuário no banco de dados
            mongo.db.usuarios.insert_one({'username': username, 'email': email, 'password': hashed_password})
        
            return redirect(url_for('login'))
        except Exception as e:
            # Log detalhado para entender o erro
            print(f"Erro ao registrar o usuário: {str(e)}")
            return f"Erro ao acessar o banco de dados: {str(e)}", 500

    return render_template('registro.html')


if __name__ == '__main__':
    # Cria a coleção 'usuarios' antes de iniciar o servidor
    create_collections()
    app.run(debug=True, port=5001)
