from flask import Blueprint, render_template, request, redirect, url_for
from app import mysql

clientes_bp = Blueprint('clientes', __name__)

# Listar clientes
@clientes_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM clientes")
        clientes = cur.fetchall()
        cur.close()
        return render_template('clientes/index.html', clientes=clientes)
    except Exception as e:
        return f"Erro ao acessar clientes: {e}"

# Adicionar novo cliente
@clientes_bp.route('/clientes/create', methods=['GET', 'POST'])
def criar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO clientes (nome, telefone, email)
                           VALUES (%s, %s, %s)''', (nome, telefone, email))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('clientes.listar_clientes'))
        except Exception as e:
            return f"Erro ao criar cliente: {e}"
    return render_template('clientes/create.html')

# Editar cliente
@clientes_bp.route('/clientes/edit/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        try:
            cur = mysql.connection.cursor()
            cur.execute('''UPDATE clientes 
                           SET nome=%s, telefone=%s, email=%s 
                           WHERE id=%s''', (nome, telefone, email, id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('clientes.listar_clientes'))
        except Exception as e:
            return f"Erro ao atualizar cliente: {e}"

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cur.fetchone()
    cur.close()
    return render_template('clientes/edit.html', cliente=cliente)

# Excluir cliente
@clientes_bp.route('/clientes/delete/<int:id>', methods=['GET'])
def deletar_cliente(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM clientes WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('clientes.listar_clientes'))
    except Exception as e:
        return f"Erro ao excluir cliente: {e}"
