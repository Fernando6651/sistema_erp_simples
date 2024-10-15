from flask import Flask
from flask_mysqldb import MySQL
from .config import Config
from app.routes.main import main_bp  # Importe o blueprint

# Inicializa a aplicação Flask
app = Flask(__name__)

app.register_blueprint(main_bp)

# Carregar as configurações do arquivo config.py
app.config.from_object(Config)

# Inicializar o MySQL
mysql = MySQL(app)

from app.routes.vendas import vendas_bp
from app.routes.estoque import estoque_bp
from app.routes.compras import compras_bp
from app.routes.financeiro import financeiro_bp
from app.routes.clientes import clientes_bp  # Novo
from app.routes.fornecedores import fornecedores_bp  # Novo

app.register_blueprint(vendas_bp)
app.register_blueprint(estoque_bp)
app.register_blueprint(compras_bp)
app.register_blueprint(financeiro_bp)
app.register_blueprint(clientes_bp)  # Novo
app.register_blueprint(fornecedores_bp)  # Novo

# Rodar a aplicação em modo debug
if __name__ == '__main__':
    app.run(debug=True)
