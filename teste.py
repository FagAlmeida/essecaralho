from pymongo import MongoClient

uri = "mongodb+srv://fagalmeida:1234@cluster0.xm9sz.mongodb.net/"
client = MongoClient(uri)

try:
    db = client["meu_banco"]  # Substitua pelo nome real do seu banco
    print("Conexão bem-sucedida! Bancos disponíveis:", client.list_database_names())
except Exception as e:
    print("Erro ao conectar ao MongoDB:", e)
