# MongoChat-Silo API

A high-performance Flask-based API for storing and retrieving chat messages using MongoDB.

## 🚀 Features
- Store peer-to-peer chat messages.
- Retrieve full chat history between two users.
- Fetch all messages for a specific user.
- Automatic room ID generation for quick querying.
- Time-sorted message retrieval.

## 📊 Database Schema MongoDB

The messages are stored in a collection named `messages` within the `chat_database`.

| Field         | Type      | Description                                      |
|--------------|-----------|--------------------------------------------------|
| `_id`        | ObjectId  | Unique identifier for each message.              |
| `sender_id`  | String    | ID of the user sending the message.              |
| `receiver_id`| String    | ID of the user receiving the message.            |
| `room_id`    | String    | Composite ID for the conversation (Peer-to-Peer).|
| `text`       | String    | The actual content of the message.               |
| `timestamp`  | ISO Date  | UTC timestamp of when the message was sent.      |

### Example Document:
```json
{
  "_id": "64f1a2b3c4d5e6f7a8b9c0d1",
  "sender_id": "user_123",
  "receiver_id": "user_456",
  "room_id": "user_123_user_456",
  "text": "Hello, how are you?",
  "timestamp": "2024-03-20T10:00:00Z"
}
```

## 🛠️ API Endpoints

### 1. Store Message
`POST /messages`
```json
{
  "sender_id": "alice",
  "receiver_id": "bob",
  "text": "Hey bob!"
}
```

### 2. Get Chat History (Between 2 Users)
`GET /history/<user1_id>/<user2_id>`

### 3. Get All Messages for a User
`GET /messages/<user_id>`

## ⚙️ Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Update `.env` with your MongoDB connection string.

3. **Run the Server:**
   ```bash
   python app.py
   ```
