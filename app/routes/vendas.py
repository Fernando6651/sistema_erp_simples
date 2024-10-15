from flask import Blueprint, render_template, request, redirect, url_for
from app import mysql

vendas_bp = Blueprint('vendas', __name__)

# Listar Vendas
@vendas_bp.route('/vendas', methods=['GET'])
def index():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT vendas.id, clientes.nome AS cliente_nome, produtos.nome AS produto_nome, vendas.quantidade, vendas.valor_total, vendas.data_venda FROM vendas JOIN clientes ON vendas.cliente_id = clientes.id JOIN produtos ON vendas.produto_id = produtos.id")
        vendas = cur.fetchall()
        cur.close()
        return render_template('vendas/index.html', vendas=vendas)
    except Exception as e:
        return f"Erro ao acessar a página de vendas: {e}"

# Adicionar nova venda
@vendas_bp.route('/vendas/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        produto_id = request.form['produto_id']
        quantidade = request.form['quantidade']
        valor_total = request.form['valor_total']
        data_venda = request.form['data_venda']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''
                INSERT INTO vendas (cliente_id, produto_id, quantidade, valor_total, data_venda)
                VALUES (%s, %s, %s, %s, %s)
            ''', (cliente_id, produto_id, quantidade, valor_total, data_venda))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('vendas.index'))
        except Exception as e:
            return f"Erro ao adicionar venda: {e}"

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nome FROM clientes")
        clientes = cur.fetchall()

        cur.execute("SELECT id, nome FROM produtos")
        produtos = cur.fetchall()

        cur.close()
        return render_template('vendas/create.html', clientes=clientes, produtos=produtos)
    except Exception as e:
        return f"Erro ao carregar formulário: {e}"

# Editar venda
@vendas_bp.route('/vendas/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        produto_id = request.form['produto_id']
        quantidade = request.form['quantidade']
        valor_total = request.form['valor_total']
        data_venda = request.form['data_venda']

        try:
            cur = mysql.connection.cursor()
            cur.execute('''
                UPDATE vendas 
                SET cliente_id=%s, produto_id=%s, quantidade=%s, valor_total=%s, data_venda=%s
                WHERE id=%s
            ''', (cliente_id, produto_id, quantidade, valor_total, data_venda, id))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('vendas.index'))
        except Exception as e:
            return f"Erro ao editar venda: {e}"

    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM vendas WHERE id=%s", (id,))
        venda = cur.fetchone()

        cur.execute("SELECT id, nome FROM clientes")
        clientes = cur.fetchall()

        cur.execute("SELECT id, nome FROM produtos")
        produtos = cur.fetchall()

        cur.close()
        return render_template('vendas/edit.html', venda=venda, clientes=clientes, produtos=produtos)
    except Exception as e:
        return f"Erro ao carregar formulário de edição: {e}"

# Excluir venda
@vendas_bp.route('/vendas/delete/<int:id>', methods=['GET'])
def delete(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM vendas WHERE id=%s", (id,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('vendas.index'))
    except Exception as e:
        return f"Erro ao excluir venda: {e}"
