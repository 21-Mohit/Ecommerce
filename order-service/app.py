import requests
import pika
import json
from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# MongoDB connection
client = MongoClient("mongodb+srv://palmohit897:1234567890@cluster0.tbarxzw.mongodb.net/")
db = client['ecommerce']
orders_collection = db['orders']

# RabbitMQ connection
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='order_events')

# Service URLs
PRODUCT_SERVICE_URL = 'http://product-service:5001'
USER_SERVICE_URL = 'http://user-service:5002'

@app.route('/orders', methods=['POST'])
@jwt_required()  # Protect this endpoint with JWT authentication
def create_order():
    """
    Create a new order (requires authentication).
    """
    data = request.json
    user_id = get_jwt_identity()  # Get the user ID from the JWT

    # Validate product and check stock
    product_id = data['product_id']
    response = requests.get(f'{PRODUCT_SERVICE_URL}/products/{product_id}')
    if response.status_code != 200:
        return jsonify({'error': 'Product not found'}), 404

    product = response.json()
    if product['stock'] < data['quantity']:
        return jsonify({'error': 'Insufficient stock'}), 400

    # Create the order
    order = {
        'id': data['id'],
        'user_id': user_id,
        'product_id': data['product_id'],
        'quantity': data['quantity'],
        'status': 'Pending'
    }
    orders_collection.insert_one(order)

    # Update product stock
    updated_stock = product['stock'] - data['quantity']
    requests.put(f'{PRODUCT_SERVICE_URL}/products/{product_id}', json={'stock': updated_stock})

    # Publish order event to RabbitMQ
    event = {
        'event_type': 'order_created',
        'order_id': order['id'],
        'user_id': user_id
    }
    channel.basic_publish(exchange='', routing_key='order_events', body=json.dumps(event)))

    return jsonify({'id': order['id']}), 201

@app.route('/orders', methods=['GET'])
@jwt_required()  # Protect this endpoint with JWT authentication
def get_orders():
    """
    Get all orders for the authenticated user.
    """
    user_id = get_jwt_identity()
    orders = list(orders_collection.find({'user_id': user_id}, {'_id': 0}))
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)