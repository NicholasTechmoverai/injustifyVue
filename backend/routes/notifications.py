from flask import Blueprint,Response,request,jsonify
notifications_bp = Blueprint('notifications', __name__)

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

@notifications_bp.route('<useremail>')
def get_notifications(useremail):
    return jsonify({"notifications": notifications.get(useremail, [])})
