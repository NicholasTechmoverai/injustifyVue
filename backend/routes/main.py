from flask import Blueprint,Response,request,jsonify
main_bp = Blueprint('main', __name__)
from utils.userDb import validate_user_login
users = {
    "kariuki12nicholas@gmail.com": {
        "name": "John Doe",
        "email": "kariuki12nicholas@gmail.com",
        "role": "member",
        "join_date": "2022-01-15",
        "last_login": "2024-02-16 12:45:30",
        "bio": "A passionate software developer and tech enthusiast.",
        "password": "0000"  # Added password
    },
    "admin@example.com": {
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "admin",
        "join_date": "2021-06-30",
        "last_login": "2024-02-16 08:30:00",
        "bio": "Managing the platform with a focus on security and performance.",
        "password": "adminpassword"  # Added password
    },
}

@main_bp.route('<useremail>')
def get_home(useremail):
    return jsonify({"message": f"Welcome, {users.get(useremail, {}).get('name', 'Guest')}!"})



@main_bp.route('/login', methods=['POST'])
def login():
    # Getting user data from the request body
    user_data = request.get_json()
    useremail = user_data.get('email')
    password = user_data.get('password')

    # Check if the email and password exist in the data
    if useremail and password:
        user = validate_user_login(useremail,password)
        if user.get('userFound') and user.get('truepassword'):
            return jsonify({"message": "Login successful", "user": user.get('user_info').get('user_info')}), 200
        elif user.get('userFound') and not user.get('truepassword'):
            return jsonify({"message": "Invalid password. Please try again."}), 401
        elif not user.get('userFound'):
            return jsonify({"message": "User not found. Please check your email."}), 404
        else:
            return jsonify({"message": "Invalid credentials. Please check your email and password."}), 401
    else:
        return jsonify({"message": "Please provide both email and password"}), 400
    


