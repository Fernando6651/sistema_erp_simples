from flask import Blueprint, render_template, request, redirect, url_for
from app import mysql

estoque_bp = Blueprint('estoque', __name__)

# Listar produtos no estoque
@estoque_bp.route('/estoque', methods=['GET'])
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM produtos")
        produtos = cur.fetchall()
        cur.close()
        return render_template('estoque/index.html', produtos=produtos)
    except Exception as e:
        return f"Erro ao acessar produtos: {e}"

# Adicionar novo produto
@estoque_bp.route('/estoque/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade_estoque = request.form['quantidade_estoque']
        preco_venda = request.form['preco_venda']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''INSERT INTO produtos (nome, quantidade_estoque, preco_venda)
                           VALUES (%s, %s, %s)''', (nome, quantidade_estoque, preco_venda))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('estoque.index'))
        except Exception as e:
            return f"Erro ao adicionar produto: {e}"

    return render_template('estoque/create.html')

# Editar produto no estoque
@estoque_bp.route('/estoque/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        nome = request.form['nome']
        quantidade_estoque = request.form['quantidade_estoque']
        preco_venda = request.form['preco_venda']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''UPDATE produtos 
                           SET nome=%s, quantidade_estoque=%s, preco_venda=%s 
                           WHERE id=%s''', (nome, quantidade_estoque, preco_venda, id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('estoque.index'))
        except Exception as e:
            return f"Erro ao atualizar produto: {e}"

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM produtos WHERE id=%s", (id,))
        produto = cur.fetchone()
        cur.close()
        return render_template('estoque/edit.html', produto=produto)
    except Exception as e:
        return f"Erro ao acessar produto: {e}"

# Excluir produto
@estoque_bp.route('/estoque/delete/<int:id>', methods=['GET'])
def delete(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM produtos WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('estoque.index'))
    except Exception as e:
        return f"Erro ao excluir produto: {e}"
