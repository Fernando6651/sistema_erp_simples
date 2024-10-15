from app import mysql
from flask_mysqldb import MySQLdb

# Função para criar uma venda
def criar_venda(cliente_id, produto_id, quantidade, valor_total, data_venda):
    try:
        # Cria um cursor simples (não precisa do DictCursor para inserções)
        cur = mysql.connection.cursor()

        # Executa a inserção na tabela 'vendas'
        cur.execute('''INSERT INTO vendas (cliente_id, produto_id, quantidade, valor_total, data_venda)
                       VALUES (%s, %s, %s, %s, %s)''', 
                    (cliente_id, produto_id, quantidade, valor_total, data_venda))

        # Confirma a transação
        mysql.connection.commit()

    except MySQLdb.Error as e:
        # Em caso de erro, registre o erro (opcionalmente faça logging)
        print(f"Erro ao inserir venda: {e}")
        return False  # Retorna False para indicar que houve um erro

    finally:
        # Garante que o cursor será fechado, mesmo em caso de erro
        cur.close()

    return True  # Retorna True se tudo ocorrer bem
