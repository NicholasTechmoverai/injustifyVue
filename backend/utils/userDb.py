import logging
from werkzeug.security import check_password_hash, generate_password_hash
logging.basicConfig(level=logging.INFO)
from config import Config

mydb = Config.mydb
mycursor = mydb.cursor()

def fetch_user(user_id):
    if not user_id:
        return {
            "success": False,
            "message": "User ID is required"
        }

    if '@' in user_id and '.' in user_id:
        select = 'email'
    else:
        select = 'id'

    try:
        query = f"SELECT * FROM injustifyUsers WHERE {select} = %s"
        mycursor.execute(query, (user_id,))
        user = mycursor.fetchone()

        if user:
            userD= {
                'success': True,
                "id": user[1],
                "email": user[0],
                "name": user[2],
                "picture": f"{Config.profilePath}/{user[3]}",
                "verified_email": user[4],
                "created_at": user[6]
            }
            return {
                'success': True,
                "message": "User  found",
                "user_info": userD
            }
        else:
            return {
                'success': False,
                "message": "User not found"
            }
    except Exception as err:
        logging.error("Error: %s", err)
        return {"success": False, "error": "An unexpected error occurred"}


def validate_user_login(email, password):
    try:
        mycursor.execute(
            "SELECT email, password FROM injustifyUsers WHERE email = %s",
            (email,)
        )
        user = mycursor.fetchone()

        if user is None:
            return {"userFound": False}

        db_email, db_password = user

        # Compare hashed password
        if check_password_hash(db_password, password):
            return {"user_info": fetch_user(db_email), "userFound": True, "truepassword": True}

        return {"user_info": None, "userFound": True, "truepassword": False}
    except Exception as err:
        logging.error("Error validating user login: %s", err)
        return {"error": "An error occurred during login validation"}

