from flask import Blueprint, render_template

# Cria o Blueprint para as rotas principais
main_bp = Blueprint('main', __name__)

# Rota para a página inicial (index)
@main_bp.route('/')
def index():
    return render_template('index.html')
