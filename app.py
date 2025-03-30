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
app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        print(f"Tentando login com usuário: {username}")  # Log para depuração

        try:
            # Verifica se a conexão com o banco de dados foi bem-sucedida
            if 'db' not in globals() or db is None:
                raise Exception("Banco de dados não conectado.")
            
            print("Conexão com o MongoDB está ativa.")  # Log para depuração

            # Procura o usuário no banco de dados MongoDB
            user = db.usuarios.find_one({'username': username})
            if not user:
                flash("Usuário não encontrado", 'error')  # Mensagem de erro com flash
                return render_template('login.html')

            print(f"Usuário encontrado: {user}")  # Log para depuração

            # Verifica se a senha corresponde ao hash armazenado
            if check_password_hash(user.get('password', ''), password):
                flash("Login bem-sucedido", 'success')  # Mensagem de sucesso com flash
                return redirect(url_for('inicio'))  # Redireciona para a página inicial
            else:
                flash("Usuário ou senha inválidos", 'error')  # Mensagem de erro com flash
                return render_template('login.html')

        except Exception as e:
            print(f"Erro no login: {str(e)}")  # Log do erro
            flash(f"Erro ao acessar o banco de dados: {str(e)}", 'error')
            return render_template('login.html')

    # Para a requisição GET, exibe o formulário de login
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
    app.run(debug=True)
