import os
import mysql.connector
from mysql.connector import pooling
import pymysql

class Config:
    # Load sensitive values from environment variables
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # Secure session cookies in production
    SESSION_COOKIE_SECURE = os.getenv("FLASK_ENV") == "production"

    thumbnailPath = "http://127.0.0.1:5000/static/thumbnails"
    profilePath = "http://127.0.0.1:5000/static/uploads"

    # Allowed CORS origins
    CORS_ALLOWED_ORIGINS = [
        "http://example.com",
        "http://192.168.100.2:5000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:8080/",
        "http://192.168.100.2:8080/"
    ]



    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="0000",
        database="injustify"
    )

