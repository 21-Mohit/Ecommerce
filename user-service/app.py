from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)

# JWT Configuration
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Secret key for signing JWTs
jwt = JWTManager(app)

# MongoDB connection
client = MongoClient("mongodb+srv://palmohit897:1234567890@cluster0.tbarxzw.mongodb.net/")  # Connect to MongoDB
db = client['ecommerce']
users_collection = db['users']

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    """
    data = request.json
    user = {
        'id': data['id'],
        'username': data['username'],
        'password': data['password']
    }
    users_collection.insert_one(user)  # Insert user into MongoDB
    return jsonify({'id': user['id']}), 201

@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and issue a JWT.
    """
    data = request.json
    user = users_collection.find_one({'username': data['username'], 'password': data['password']}, {'_id': 0})
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create a JWT token with the user's ID as the identity
    access_token = create_access_token(identity=user['id'])
    return jsonify({'access_token': access_token}), 200

@app.route('/users/<int:id>', methods=['GET'])
@jwt_required()  # Protect this endpoint with JWT authentication
def get_user(id):
    """
    Get user details (requires authentication).
    """
    user = users_collection.find_one({'id': id}, {'_id': 0})
    if user:
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)  # Run the Flask app