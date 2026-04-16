from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client['chat_database']
messages_collection = db['messages']

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "alive"}), 200

@app.route('/messages', methods=['POST'])
def store_message():
    data = request.json
    
    required_fields = ['sender_id', 'receiver_id', 'text']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    message = {
        "sender_id": data['sender_id'],
        "receiver_id": data['receiver_id'],
        "room_id": data.get('room_id', f"{min(data['sender_id'], data['receiver_id'])}_{max(data['sender_id'], data['receiver_id'])}"),
        "text": data['text'],
        "timestamp": datetime.utcnow()
    }
    
    result = messages_collection.insert_one(message)
    message['_id'] = str(result.inserted_id)
    
    return jsonify({"message": "Message stored successfully", "data": message}), 201

@app.route('/messages/<user_id>', methods=['GET'])
def get_user_messages(user_id):
    # Get all messages where user is either sender or receiver
    messages = list(messages_collection.find({
        "$or": [
            {"sender_id": user_id},
            {"receiver_id": user_id}
        ]
    }).sort("timestamp", 1))
    
    for msg in messages:
        msg['_id'] = str(msg['_id'])
        
    return jsonify(messages), 200

@app.route('/history/<user1_id>/<user2_id>', methods=['GET'])
def get_chat_history(user1_id, user2_id):
    # Get messages between two specific users
    messages = list(messages_collection.find({
        "$or": [
            {"sender_id": user1_id, "receiver_id": user2_id},
            {"sender_id": user2_id, "receiver_id": user1_id}
        ]
    }).sort("timestamp", 1))
    
    for msg in messages:
        msg['_id'] = str(msg['_id'])
        
    return jsonify(messages), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
