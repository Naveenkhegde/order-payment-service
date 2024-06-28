from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# Connect to MySQL database
cnx = mysql.connector.connect(
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', 'password'),
    host=os.getenv('MYSQL_HOST', 'mysql-service'),
    database=os.getenv('MYSQL_DATABASE', 'orders')
)
cursor = cnx.cursor(dictionary=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/orders', methods=['GET'])
def get_orders():
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    return render_template('order.html', orders=orders)

@app.route('/orders', methods=['POST'])
def create_order():
    name = request.form['name']
    quantity = request.form['quantity']
    cursor.execute("INSERT INTO orders (name, quantity) VALUES (%s, %s)", (name, quantity))
    cnx.commit()
    return redirect(url_for('get_orders'))

@app.route('/payments', methods=['GET'])
def get_payments():
    cursor.execute("SELECT * FROM payments")
    payments = cursor.fetchall()
    return render_template('payment.html', payments=payments)

@app.route('/payments', methods=['POST'])
def create_payment():
    order_id = request.form['order_id']
    amount = request.form['amount']
    cursor.execute("INSERT INTO payments (order_id, amount) VALUES (%s, %s)", (order_id, amount))
    cnx.commit()
    return redirect(url_for('get_payments'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
