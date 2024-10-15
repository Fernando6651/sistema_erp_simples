from flask import Blueprint, render_template, request, redirect, url_for
from app import mysql

financeiro_bp = Blueprint('financeiro', __name__)

# Listar transações financeiras
@financeiro_bp.route('/financeiro', methods=['GET'])
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM financeiro")
        transacoes = cur.fetchall()
        cur.close()
        return render_template('financeiro/index.html', transacoes=transacoes)
    except Exception as e:
        return f"Erro ao acessar o relatório financeiro: {e}"

# Adicionar nova transação
@financeiro_bp.route('/financeiro/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        tipo = request.form['tipo']
        valor = request.form['valor']
        descricao = request.form['descricao']
        data = request.form['data']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO financeiro (tipo, valor, descricao, data)
                           VALUES (%s, %s, %s, %s)''', (tipo, valor, descricao, data))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('financeiro.index'))
        except Exception as e:
            return f"Erro ao adicionar a transação financeira: {e}"

    return render_template('financeiro/create.html')

# Editar transação
@financeiro_bp.route('/financeiro/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        tipo = request.form['tipo']
        valor = request.form['valor']
        descricao = request.form['descricao']
        data = request.form['data']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''UPDATE financeiro 
                           SET tipo=%s, valor=%s, descricao=%s, data=%s 
                           WHERE id=%s''', (tipo, valor, descricao, data, id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('financeiro.index'))
        except Exception as e:
            return f"Erro ao atualizar a transação financeira: {e}"

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM financeiro WHERE id=%s", (id,))
        transacao = cur.fetchone()
        cur.close()
        return render_template('financeiro/edit.html', transacao=transacao)
    except Exception as e:
        return f"Erro ao acessar a transação financeira: {e}"

# Excluir transação
@financeiro_bp.route('/financeiro/delete/<int:id>', methods=['GET'])
def delete(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM financeiro WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('financeiro.index'))
    except Exception as e:
        return f"Erro ao excluir a transação financeira: {e}"
