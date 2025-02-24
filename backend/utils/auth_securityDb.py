import logging
from datetime import datetime,timedelta

logging.basicConfig(level=logging.INFO)
from config import Config

mydb = Config.mydb
mycursor = mydb.cursor()


def set_token(email, token):
    try:
        # Check if a token exists for this email
        mycursor.execute(
            "SELECT email, expires_at FROM verification_sessions WHERE email = %s",
            (email,)
        )
        result = mycursor.fetchone()

        # If a token exists, check if it is expired
        if result:
            expires_at = result[1]

            # If the token is expired, delete it and proceed with setting the new token
            if datetime.utcnow() > expires_at:
                # Delete the expired token
                mycursor.execute(
                    "DELETE FROM verification_sessions WHERE email = %s",
                    (email,)
                )
                mydb.commit()

            else:
                return {"success": False, "message": "A valid token already exists for this email."}

        # Calculate expiration time for the new token (10 minutes from now)
        expires_at = datetime.utcnow() + timedelta(minutes=10)

        # Insert the new token
        mycursor.execute(
            "INSERT INTO verification_sessions (email, token, expires_at) VALUES (%s, %s, %s)",
            (email, token, expires_at)
        )
        mydb.commit()
        return {"success": True, "message": "Token sent successfully!"}

    except Exception as e:
        # Log the exception and return a generic error message
        print(f"Error setting token: {e}")
        return {"success": False, "message": "An error occurred while setting the token."}
