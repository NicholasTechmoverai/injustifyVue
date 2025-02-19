from flask import Blueprint,Response,request,jsonify
history_bp = Blueprint('history', __name__)

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

@history_bp.route('<useremail>')
def get_history(useremail):
    return jsonify({"history": history.get(useremail, [])})
