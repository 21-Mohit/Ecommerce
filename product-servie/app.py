from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, jwt_required

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'super-secret-key'
jwt = JWTManager(app)

# MongoDB connection
client = MongoClient("mongodb+srv://palmohit897:1234567890@cluster0.tbarxzw.mongodb.net/")   ## Need to update the mongo db url.
db = client['ecommerce']
products_collection = db['products']

@app.route('/products', methods=['GET'])
def get_products():
    """
    Get all products.
    """
    products = list(products_collection.find({}, {'_id': 0}))
    return jsonify(products)

@app.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    """
    Get a specific product by ID.
    """
    product = products_collection.find_one({'id': id}, {'_id': 0})
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

@app.route('/products', methods=['POST'])
@jwt_required()  # Protect this endpoint with JWT authentication
def create_product():
    """
    Create a new product (requires authentication).
    """
    data = request.json
    product = {
        'id': data['id'],
        'name': data['name'],
        'price': data['price'],
        'stock': data['stock']
    }
    products_collection.insert_one(product)
    return jsonify({'id': product['id']}), 201

@app.route('/products/<int:id>', methods=['PUT'])
@jwt_required()  # Protect this endpoint with JWT authentication
def update_product(id):
    """
    Update a product (requires authentication).
    """
    data = request.json
    products_collection.update_one({'id': id}, {'$set': data})
    return jsonify({'message': 'Product updated'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)