from flask import Blueprint,Response,request,jsonify
import logging
from config import Config
from utils.userDb import fetch_user

mydb = Config.mydb
mycursor = mydb.cursor()


profile_bp = Blueprint('profile', __name__)

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

@profile_bp.route('<useremail>')
def get_profile(useremail):
    print("GET request for user profile: {useremail}")
    return jsonify(fetch_user(useremail).get("user_info", {}))

