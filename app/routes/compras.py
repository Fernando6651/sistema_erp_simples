from flask import Blueprint, render_template, request, redirect, url_for
from app import mysql

compras_bp = Blueprint('compras', __name__)

# Listar compras
@compras_bp.route('/compras', methods=['GET'])
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT compras.id, fornecedores.nome AS fornecedor_nome, produtos.nome AS produto_nome, 
                   compras.quantidade, compras.valor_total, compras.data_compra 
            FROM compras
            JOIN fornecedores ON compras.fornecedor_id = fornecedores.id
            JOIN produtos ON compras.produto_id = produtos.id
        """)
        compras = cur.fetchall()
        cur.close()
        return render_template('compras/index.html', compras=compras)
    except Exception as e:
        return f"Erro ao acessar as compras: {e}"

# Adicionar nova compra
@compras_bp.route('/compras/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        fornecedor_id = request.form['fornecedor_id']
        produto_id = request.form['produto_id']
        quantidade = request.form['quantidade']
        valor_total = request.form['valor_total']
        data_compra = request.form['data_compra']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''
                INSERT INTO compras (fornecedor_id, produto_id, quantidade, valor_total, data_compra)
                VALUES (%s, %s, %s, %s, %s)
            ''', (fornecedor_id, produto_id, quantidade, valor_total, data_compra))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('compras.index'))
        except Exception as e:
            return f"Erro ao adicionar compra: {e}"

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nome FROM fornecedores")
        fornecedores = cur.fetchall()

        cur.execute("SELECT id, nome FROM produtos")
        produtos = cur.fetchall()

        cur.close()
        return render_template('compras/create.html', fornecedores=fornecedores, produtos=produtos)
    except Exception as e:
        return f"Erro ao carregar formulário de compra: {e}"

# Editar compra
@compras_bp.route('/compras/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        fornecedor_id = request.form['fornecedor_id']
        produto_id = request.form['produto_id']
        quantidade = request.form['quantidade']
        valor_total = request.form['valor_total']
        data_compra = request.form['data_compra']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE compras 
                SET fornecedor_id=%s, produto_id=%s, quantidade=%s, valor_total=%s, data_compra=%s
                WHERE id=%s
            ''', (fornecedor_id, produto_id, quantidade, valor_total, data_compra, id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('compras.index'))
        except Exception as e:
            return f"Erro ao editar compra: {e}"

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM compras WHERE id=%s", (id,))
        compra = cur.fetchone()

        cur.execute("SELECT id, nome FROM fornecedores")
        fornecedores = cur.fetchall()

        cur.execute("SELECT id, nome FROM produtos")
        produtos = cur.fetchall()

        cur.close()
        return render_template('compras/edit.html', compra=compra, fornecedores=fornecedores, produtos=produtos)
    except Exception as e:
        return f"Erro ao carregar formulário de edição: {e}"

# Excluir compra
@compras_bp.route('/compras/delete/<int:id>', methods=['GET'])
def delete(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM compras WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('compras.index'))
    except Exception as e:
        return f"Erro ao excluir compra: {e}"
