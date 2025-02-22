import os
import random
import logging
import smtplib
import datetime as dl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flask import (
    Blueprint, Response, request, jsonify, session, redirect, url_for, current_app
)
from authlib.integrations.flask_client import OAuth
from google.oauth2 import id_token
from google.auth.transport import requests
from utils.userDb import validate_user_login, validate_user, createNewUser, fetch_user

from config import Config

main_bp = Blueprint('main', __name__)

# Load environment variables
load_dotenv()
EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
MY_ID = os.getenv("MY_ID")
MY_SECRET = os.getenv("MY_SECRET")

if not MY_ID or not MY_SECRET:
    raise ValueError("Google OAuth credentials (MY_ID and MY_SECRET) must be set in the environment variables.")

# Configure OAuth
oauth = OAuth(current_app)
google = oauth.register(
    name='google',
    client_id=MY_ID,
    client_secret=MY_SECRET,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    access_token_url='https://oauth2.googleapis.com/token',
    redirect_uri='http://127.0.0.1:5000/login/callback',
    client_kwargs={'scope': 'openid email profile', 'state': True},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
)

# Mock User Data (For Testing Purposes)
users = {
    "kariuki12nicholas@gmail.com": {
        "name": "John Doe",
        "email": "kariuki12nicholas@gmail.com",
        "role": "member",
        "join_date": "2022-01-15",
        "last_login": "2024-02-16 12:45:30",
        "bio": "A passionate software developer and tech enthusiast.",
        "password": "0000"
    },
    "admin@example.com": {
        "name": "Admin User",
        "email": "admin@example.com",
        "role": "admin",
        "join_date": "2021-06-30",
        "last_login": "2024-02-16 08:30:00",
        "bio": "Managing the platform with a focus on security and performance.",
        "password": "adminpassword"
    },
}

# Routes
@main_bp.route('/<useremail>')
def get_home(useremail):
    return jsonify({"message": f"Welcome, {users.get(useremail, {}).get('name', 'Guest')}!"})

@main_bp.route('/login', methods=['POST'])
def login():
    user_data = request.get_json()
    useremail = user_data.get('email')
    password = user_data.get('password')
    
    if useremail and password:
        user = validate_user_login(useremail, password)
        if user.get('userFound'):
            if user.get('truepassword'):
                return jsonify({"message": "Login successful", "user": user.get('user_info').get('user_info')}), 200
            return jsonify({"message": "Invalid password. Please try again."}), 401
        return jsonify({"message": "User not found. Please check your email."}), 404
    return jsonify({"message": "Please provide both email and password"}), 400

@main_bp.route('/login/google')
def google_login():
    try:
        redirect_uri = url_for('main.authorize_route', _external=True)
        return google.authorize_redirect(redirect_uri)
    except Exception as e:
        logging.error(f"Login error: {e}")
        return "An error occurred during login redirection.", 500

from urllib.parse import urlencode
import json
from urllib.parse import urlencode


@main_bp.route('/login/callback')
def authorize_route():
    try:
        token = google.authorize_access_token()
        if not token:
            return redirect(f"{Config.FRONTEND_SERVER}/login?error=access_token_failed")  # Redirect to frontend with error
        
        user_info_response = google.get('https://www.googleapis.com/oauth2/v1/userinfo')
        if user_info_response.status_code != 200:
            return redirect(f"{Config.FRONTEND_SERVER}/login?error=user_info_failed")
        
        user_info = user_info_response.json()
        user_email = user_info.get('email')
        if not user_email:
            return redirect(f"{Config.FRONTEND_SERVER}/login?error=email_missing")
        
        # Fetch user details from database
        user_data = fetch_user(user_email).get('user_info')

        if not validate_user(user_email):
            createNewUser(user_info)  # Create new user if not exists
            user_data = fetch_user(user_email).get('user_info')


        query_params = urlencode({
        "message": "Login successful",
        "user": json.dumps(user_data, default=str)  # Convert to JSON and serialize datetime
        })

        return redirect(f"{Config.FRONTEND_SERVER}/dashboard?{query_params}")
    
    except Exception as e:
        logging.error(f"Authorization error: {e}")
        return redirect(f"{Config.FRONTEND_SERVER}/login?error=server_error")



@main_bp.route('/logout')
def logout_route():
    session.clear()
    return redirect(url_for('main.noindexx'))

@main_bp.route('/verify-token', methods=['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('token')
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            '507627163964-ms3hgtil3pe68bgsih6n6545t0lh2r91.apps.googleusercontent.com'
        )
        user_info = {"email": idinfo['email'], "name": idinfo.get('name', 'Unknown'), "picture": idinfo.get('picture', '')}
        return jsonify(success=True, user=user_info)
    except ValueError:
        return jsonify(success=False), 400
