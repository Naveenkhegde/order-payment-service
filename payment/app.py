from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Connect to MySQL database
cnx = mysql.connector.connect(
    user='root',
    password='password',
    host='mysql-service',
    database='orders'
)
cursor = cnx.cursor()

@app.route('/payments', methods=['GET'])
def get_payments():
    cursor.execute("SELECT * FROM payments")
    payments = cursor.fetchall()
    return jsonify([dict(payment) for payment in payments])

@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    cursor.execute("INSERT INTO payments (amount, order_id) VALUES (%s, %s)", (data['amount'], data['order_id']))
    cnx.commit()
    return jsonify({'message': 'Payment created successfully'})

if __name__ == '__main__':
    app.run(debug=True)
