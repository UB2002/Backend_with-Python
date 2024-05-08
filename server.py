#server.py
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
client = None
collection = None

# Function to connect to MongoDB
def connect_to_mongodb():
    global client, collection
    try:
        client = MongoClient('mongodb+srv://udaybhaskarmathangi:mX0W7b1UMwwUP6Ph@ub2002.carusdb.mongodb.net/?retryWrites=true&w=majority&appName=UB2002')
        db = client.get_database('Node-API')
        collection = db['items']
        print("Connected to MongoDB")
    except Exception as e:
        print("Failed to connect to MongoDB:", e)

# Check MongoDB connection when the application starts
connect_to_mongodb()

# Route for the root URL
@app.route('/')
def index():
    return 'Welcome to the CRUD API!'

# Create
@app.route('/items', methods=['POST'])
def create_item():
    if client:
        data = request.json
        item_id = collection.insert_one(data).inserted_id
        return jsonify(str(item_id))
    else:
        return jsonify({'error': 'Failed to connect to MongoDB'})

# Read
@app.route('/items', methods=['GET'])
def get_all_items():
    if client:
        items = list(collection.find())
        # Convert ObjectId to string for serialization
        for item in items:
            item['_id'] = str(item['_id'])
        return jsonify(items)
    else:
        return jsonify({'error': 'Failed to connect to MongoDB'})

@app.route('/items/<id>', methods=['GET'])
def get_item(id):
    if client:
        item = collection.find_one({'_id': ObjectId(id)})
        if item:
            # Convert ObjectId to string for serialization
            item['_id'] = str(item['_id'])
            return jsonify(item)
        else:
            return jsonify({'error': 'Item not found'}), 404
    else:
        return jsonify({'error': 'Failed to connect to MongoDB'})

# Update
@app.route('/items/<id>', methods=['PUT'])
def update_item(id):
    if client:
        data = request.json
        updated_item = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        return jsonify({'message': 'Item updated successfully'})
    else:
        return jsonify({'error': 'Failed to connect to MongoDB'})

# Delete
@app.route('/items/<id>', methods=['DELETE'])
def delete_item(id):
    if client:
        collection.delete_one({'_id': ObjectId(id)})
        return jsonify({'message': 'Item deleted successfully'})
    else:
        return jsonify({'error': 'Failed to connect to MongoDB'})

if __name__ == '__main__':
    app.run(debug=True)
