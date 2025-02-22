import logging
import uuid
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


def createNewUser(Userinfo):
    if Userinfo:
        id = Userinfo.get('id',None)
        name = Userinfo['name']
        password = Userinfo.get('password', None)
        email = Userinfo['email']
        profilePicture = Userinfo.get('picture', None)  # Use .get() for optional fields
        verified_email = Userinfo.get('verified_email', False)

        if not id:
            id = str(uuid.uuid4())  

        
        # Hash the password if it's provided
        if password:
            password = generate_password_hash(password)

        if not profilePicture:
            profilePicture ='static/img/icon3.jpg'  # Default profile picture


        try:
            mycursor.execute(
                "INSERT INTO injustifyUsers (id,email, name, password, picture,verified_email) VALUES (%s,%s, %s, %s, %s,%s)",
                (id,email, name,password , profilePicture, verified_email)
            )
            mydb.commit()  # Commit the transaction
            return 'success'
        except Exception as err:
            logging.error("Error: %s", err) 
            return str(err)
    return 'error'


def validate_user(user_email):
    try:
        mycursor.execute("SELECT verified_email FROM injustifyUsers WHERE email = %s", (user_email,))
        user = mycursor.fetchone()
        if user and user[0] == 1:
            return True
        else:
            return False
    except Exception as err:
        logging.error("Error: %s", err)
        return False
