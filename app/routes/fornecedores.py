from flask import Blueprint, render_template, request, redirect, url_for
from app import mysql

fornecedores_bp = Blueprint('fornecedores', __name__)

# Listar fornecedores
@fornecedores_bp.route('/fornecedores', methods=['GET'])
def listar_fornecedores():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM fornecedores")
        fornecedores = cur.fetchall()
        cur.close()
        return render_template('fornecedores/index.html', fornecedores=fornecedores)
    except Exception as e:
        return f"Erro ao acessar fornecedores: {e}"

# Adicionar fornecedor
@fornecedores_bp.route('/fornecedores/create', methods=['GET', 'POST'])
def criar_fornecedor():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO fornecedores (nome, telefone, email)
                           VALUES (%s, %s, %s)''', (nome, telefone, email))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('fornecedores.listar_fornecedores'))
        except Exception as e:
            return f"Erro ao criar fornecedor: {e}"

    return render_template('fornecedores/create.html')

# Editar fornecedor
@fornecedores_bp.route('/fornecedores/edit/<int:id>', methods=['GET', 'POST'], endpoint='editar_fornecedor')
def editar_fornecedor(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''UPDATE fornecedores 
                           SET nome=%s, telefone=%s, email=%s 
                           WHERE id=%s''', (nome, telefone, email, id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('fornecedores.listar_fornecedores'))
        except Exception as e:
            return f"Erro ao atualizar fornecedor: {e}"

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM fornecedores WHERE id=%s", (id,))
        fornecedor = cur.fetchone()
        cur.close()
        return render_template('fornecedores/edit.html', fornecedor=fornecedor)
    except Exception as e:
        return f"Erro ao acessar fornecedor: {e}"

# Excluir fornecedor
@fornecedores_bp.route('/fornecedores/delete/<int:id>', methods=['GET'])
def deletar_fornecedor(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM fornecedores WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('fornecedores.listar_fornecedores'))
    except Exception as e:
        return f"Erro ao excluir fornecedor: {e}"
