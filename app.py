from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
DATABASE = 'restaurant.db'

def create_tables():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, quantity INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM products")
        products = c.fetchall()
        conn.close()
        return jsonify(products)
    elif request.method == 'POST':
        data = request.get_json()
        name = data['name']
        price = data['price']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product added successfully'})

@app.route('/products/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product(id):
    if request.method == 'GET':
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM products WHERE id=?", (id,))
        product = c.fetchone()
        conn.close()
        return jsonify(product)
    elif request.method == 'PUT':
        data = request.get_json()
        name = data['name']
        price = data['price']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("UPDATE products SET name=?, price=? WHERE id=?", (name, price, id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product updated successfully'})
    elif request.method == 'DELETE':
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE id=?", (id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Product deleted successfully'})

@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("SELECT * FROM orders")
        orders = c.fetchall()
        conn.close()
        return jsonify(orders)
    elif request.method == 'POST':
        data = request.get_json()
        product_id = data['product_id']
        quantity = data['quantity']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute("INSERT INTO orders (product_id, quantity) VALUES (?, ?)", (product_id, quantity))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Order placed successfully'})

if __name__ == '__main__':
    create_tables()
    app.run(debug=True)
