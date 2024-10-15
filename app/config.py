import os
from dotenv import load_dotenv

# Carrega o arquivo .env
load_dotenv()

class Config:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'sua_senha')  # Substitua pela senha correta do MySQL
    MYSQL_DB = os.getenv('MYSQL_DB', 'erp_sistema')
    MYSQL_CURSORCLASS = 'DictCursor'  # Isso faz o cursor retornar resultados como dicionários
    SECRET_KEY = os.getenv('SECRET_KEY', 'minha_chave_secreta')

    # Adiciona prints para depurar as variáveis carregadas
    print(f"MYSQL_USER: {MYSQL_USER}")
    print(f"MYSQL_PASSWORD: {MYSQL_PASSWORD}")
