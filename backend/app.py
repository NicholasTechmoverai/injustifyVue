from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from websocket_service import INJUserNamespace

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

websocket = INJUserNamespace(app)
@socketio.on('connect', namespace='/ws')
def handle_connect():
    print("Client connected to WebSocket")

@socketio.on('disconnect', namespace='/ws')
def handle_disconnect():
    print("Client disconnected from WebSocket")

# Sample User Data
users = {
    "user@example.com": {
        "name": "John Doe",
        "email": "user@example.com",
        "role": "member",
        "join_date": "2022-01-15",
        "last_login": "2024-02-16 12:45:30",
        "bio": "A passionate software developer and tech enthusiast."
    },
    "admin@example.com": {
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "admin",
        "join_date": "2021-06-30",
        "last_login": "2024-02-16 08:30:00",
        "bio": "Managing the platform with a focus on security and performance."
    },
}

# Notifications Data
notifications = {
    "user@example.com": [
        {"id": 1, "message": "New message received", "date": "2024-02-15"},
        {"id": 2, "message": "Your order is ready for pickup", "date": "2024-02-14"}
    ],
    "admin@example.com": [
        {"id": 1, "message": "New admin request pending approval", "date": "2024-02-15"},
        {"id": 2, "message": "Server successfully updated", "date": "2024-02-14"}
    ],
}

# Downloads Data
downloads = {
    "user@example.com": [
        {"file": "File1.pdf", "size": "2MB", "date": "2024-02-10"},
        {"file": "Report.docx", "size": "500KB", "date": "2024-02-12"}
    ],
    "admin@example.com": [
        {"file": "Admin_Guide.pdf", "size": "3MB", "date": "2024-02-05"},
        {"file": "Security_Policies.docx", "size": "1.2MB", "date": "2024-02-08"}
    ],
}

# User History Data
history = {
    "user@example.com": [
        {"action": "Logged in", "date": "2024-02-16 12:45"},
        {"action": "Downloaded File1.pdf", "date": "2024-02-10"},
        {"action": "Updated profile info", "date": "2024-02-08"},
    ],
    "admin@example.com": [
        {"action": "Logged in", "date": "2024-02-16 08:30"},
        {"action": "Approved a new user request", "date": "2024-02-14"},
        {"action": "Updated security settings", "date": "2024-02-10"},
    ],
}

# API Routes
@app.route('/api/profile/<useremail>')
def get_profile(useremail):
    return jsonify(users.get(useremail, {"error": "User not found"}))

@app.route('/api/notifications/<useremail>')
def get_notifications(useremail):
    return jsonify({"notifications": notifications.get(useremail, [])})

@app.route('/api/downloads/<useremail>')
def get_downloads(useremail):
    return jsonify({"downloads": downloads.get(useremail, [])})

@app.route('/api/history/<useremail>')
def get_history(useremail):
    return jsonify({"history": history.get(useremail, [])})

@app.route('/api/<useremail>')
def get_home(useremail):
    return jsonify({"message": f"Welcome, {users.get(useremail, {}).get('name', 'Guest')}!"})

# WebSocket API Routes
@app.route('/api/send_notification/<useremail>/<message>')
def send_notification(useremail, message):
    """Trigger a real-time notification to a specific user."""
    websocket.send_notification(useremail, message)
    return jsonify({"status": "Notification sent"})

@app.route('/api/send_update/<useremail>/<update_type>')
def send_update(useremail, update_type):
    """Trigger a real-time update for downloads or history."""
    if update_type == "downloads":
        data = downloads.get(useremail, [])
    elif update_type == "history":
        data = history.get(useremail, [])
    else:
        return jsonify({"error": "Invalid update type"}), 400

    websocket.send_update(useremail, update_type, data)
    return jsonify({"status": "Update sent"})

# Run Flask App
if __name__ == '__main__':
    websocket.run()
