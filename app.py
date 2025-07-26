from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/clientes')
def clientes():
    conn = get_db_connection()
    clientes = conn.execute('SELECT * FROM clientes').fetchall()
    conn.close()
    return render_template('clientes.html', clientes=clientes)

@app.route('/produtos')
def produtos():
    conn = get_db_connection()
    produtos = conn.execute('SELECT * FROM produtos').fetchall()
    conn.close()
    return render_template('produtos.html', produtos=produtos)

@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    conn = get_db_connection()
    if request.method == 'POST':
        cliente_id = request.form['cliente_id']
        produto_id = request.form['produto_id']
        quantidade = int(request.form['quantidade'])
        data_venda = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn.execute('INSERT INTO vendas (cliente_id, produto_id, quantidade, data_venda) VALUES (?, ?, ?, ?)',
                     (cliente_id, produto_id, quantidade, data_venda))
        conn.commit()
        conn.close()
        return redirect(url_for('vendas'))
    else:
        clientes = conn.execute('SELECT * FROM clientes').fetchall()
        produtos = conn.execute('SELECT * FROM produtos').fetchall()
        vendas = conn.execute('SELECT v.id, c.nome as cliente, p.nome as produto, v.quantidade, v.data_venda FROM vendas v JOIN clientes c ON v.cliente_id = c.id JOIN produtos p ON v.produto_id = p.id ORDER BY v.data_venda DESC').fetchall()
        conn.close()
        return render_template('vendas.html', vendas=vendas, clientes=clientes, produtos=produtos)

@app.route('/relatorios')
def relatorios():
    conn = get_db_connection()
    relatorio = conn.execute('''
        SELECT c.nome as cliente, p.nome as produto, SUM(v.quantidade) as total_comprado
        FROM vendas v
        JOIN clientes c ON v.cliente_id = c.id
        JOIN produtos p ON v.produto_id = p.id
        GROUP BY v.cliente_id, v.produto_id
        ORDER BY cliente
    ''').fetchall()
    conn.close()
    return render_template('relatorios.html', relatorio=relatorio)

if __name__ == '__main__':
    app.run(debug=True)