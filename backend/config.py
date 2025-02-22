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
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    SONGS_FOLDER = os.path.join(BASE_DIR,'static', 'songs')

    # Allowed CORS origins
    CORS_ALLOWED_ORIGINS = [
        "http://example.com",
        "http://192.168.100.2:5000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:8080/",
        "http://192.168.100.2:8080/"
    ]

    FRONTEND_SERVER = "http://localhost:8080"



    mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="0000",
        database="injustify"
    )

    # Database connection 
    db_config = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "0000"),
        "database": os.getenv("DB_NAME", "injustify")
    }

    connection_pool = pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=int(os.getenv("DB_POOL_SIZE", 10)),  # Default to 10
        pool_reset_session=True,  # Resets session state after reuse
        autocommit=True,  # Ensures transactions are committed automatically
        **db_config
    )
    
    @staticmethod
    def get_db_connection():
        """
        Get a database connection from the pool.
        If the connection fails, return None.
        """
        try:
            return Config.connection_pool.get_connection()
        except mysql.connector.Error as e:
            print(f"Database connection failed: {e}")
            return None

