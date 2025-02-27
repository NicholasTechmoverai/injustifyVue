import logging
from datetime import datetime,timedelta

logging.basicConfig(level=logging.INFO)
from config import Config

mydb = Config.mydb
mycursor = mydb.cursor()

from datetime import datetime, timedelta

def check_token_existency(email):
    try:
        # Check if a token exists for this email
        mycursor.execute(
            "SELECT expires_at FROM verification_sessions WHERE email = %s",
            (email,)
        )
        result = mycursor.fetchone()

        if result:
            expires_at = result[0]

            # If token is expired, delete it and return False
            if datetime.utcnow() > expires_at:
                mycursor.execute(
                    "DELETE FROM verification_sessions WHERE email = %s",
                    (email,)
                )
                mydb.commit()
                return False  # Expired token was removed

            return True  # Token exists and is still valid
        
        return False  # No token found

    except Exception as e:
        print(f"Error checking token: {e}")
        return False  # Assume no valid token exists in case of error


def set_token(email, token):
    try:
        if check_token_existency(email):
            return {"success": False, "message": "A valid token already exists for the given email."}

        # Generate a new token with a 30-minute expiry
        expires_at = datetime.utcnow() + timedelta(minutes=30)
        mycursor.execute(
            "INSERT INTO verification_sessions (email, token, expires_at) VALUES (%s, %s, %s)",
            (email, token, expires_at)
        )
        mydb.commit()

        return {"success": True, "message": "Token sent successfully!"}

    except Exception as e:
        print(f"Error setting token: {e}")
        return {"success": False, "message": "An error occurred while setting the token."}

def validate_token(email, token ,delete=False):
    if not email or not token:
        return {"valid": False, "message": "Email and token are required."}

    try:
        mycursor.execute(
            "SELECT token, expires_at FROM verification_sessions WHERE email = %s",
            (email,)
        )
        result = mycursor.fetchone()

        if not result:
            return {"valid": False, "message": "No token found for the given email or the token is invalid."}

        setToken, expires_at = result

        if datetime.utcnow() > expires_at:
            mycursor.execute("DELETE FROM verification_sessions WHERE email = %s", (email,))
            mydb.commit()
            return {"valid": False, "message": "Token expired. Please sign up again."}

        if token == setToken:
            if delete:
                mycursor.execute("DELETE FROM verification_sessions WHERE email = %s", (email,))
                mydb.commit()
                
            return {"valid": True, "message": "Verification successful!"}

        return {"valid": False, "message": "Verification failed. Token mismatch."}
    
    except Exception as e:
        print(f"Error during token validation: {e}")
        return {"valid": False, "message": "An error occurred during validation. Please try again later."}

