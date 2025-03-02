import logging
import uuid
from werkzeug.security import check_password_hash, generate_password_hash
logging.basicConfig(level=logging.INFO)
from config import Config
from datetime import datetime
from typing import Optional, List, Dict, Union
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
        profilePicture = Userinfo.get('picture',  'nouser.jpeg')
        verified_email = Userinfo.get('verified_email', False)

        if not id:
            id = str(uuid.uuid4())  

        
        # Hash the password if it's provided
        if password:
            password = generate_password_hash(password)

        if not profilePicture:
            profilePicture ='nouser.jpeg'


        try:
            mycursor.execute(
                "INSERT INTO injustifyUsers (id,email, name, password, picture,verified_email) VALUES (%s,%s, %s, %s, %s,%s)",
                (id,email, name,password , profilePicture, verified_email)
            )
            mydb.commit()  
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



def update_user_password(username, password):
    if not username or not password:
        return {"success": False, "message": "Username and password are required"}
    
    try:
        password_hash = generate_password_hash(password)
        mycursor = mydb.cursor()

        query = "UPDATE injustifyUsers SET password = %s WHERE email = %s"
        mycursor.execute(query, (password_hash, username))
        mydb.commit()
        affected_rows = mycursor.rowcount  # Check if any row was updated
        mycursor.close()

        if affected_rows == 0:
            return {"success": False, "message": "No user found with that email"}

        return {"success": True, "message": "Password updated successfully"}

    except Exception as db_err:
        logging.error("Database Error: %s", db_err)
        return {"success": False, "message": f"Database error: {str(db_err)}"}

    except Exception as err:
        logging.error("Unexpected Error: %s", err)
        return {"success": False, "message": f"Unexpected error: {str(err)}"}



def fetch_downloads(
    user_id: Optional[int] = None,
    song_id: Optional[str] = None,
    name: Optional[str] = None,
    date: Optional[Union[str, datetime]] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    order_by: Optional[str] = None
) -> Optional[List[Dict]]:
    """
    Fetch downloads from the database with flexible filtering, sorting, and pagination.
    
    Args:
        user_id (Optional[int]): User ID to filter downloads.
        song_id (Optional[str]): Song ID to filter downloads.
        name (Optional[str]): Name to filter downloads.
        date (Optional[Union[str, datetime]]): Date to filter downloads.
        limit (Optional[int]): Maximum number of records to return.
        offset (Optional[int]): Number of records to skip.
        order_by (Optional[str]): Column to sort the results.

    Returns:
        Optional[List[Dict]]: List of downloads or None in case of an error.
    """
    try:
        query = "SELECT * FROM downloads WHERE 1=1"
        values = []

        if user_id:
            if '@' in user_id and '.'  in user_id:
                qr=f"SELECT id FROM injustifyusers WHERE email = %s"
                mycursor.execute(qr, (user_id,))
                user_id = mycursor.fetchone()[0]                

            query += " AND user_id = %s"
            values.append(user_id)
        
        if song_id:
            query += " AND song_id = %s"
            values.append(song_id)
        
        if name:
            query += " AND filename LIKE %s"
            values.append(f"%{name}%")
        
        if date:
            query += " AND DATE(timestamp) = %s"
            values.append(date)
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit is not None:
            query += " LIMIT %s"
            values.append(limit)
        
        if offset is not None:
            query += " OFFSET %s"
            values.append(offset)

        mycursor.execute(query, values)
        results = mycursor.fetchall()

        downloads= [{
            'filesize': result[6],
            'filename': result[3],
            'thumbnail': result[14],
            'links': result[2],
            'timestamp': result[10].strftime('%Y-%m-%d %H:%M:%S'),
        } for result in results]
        return {
            "success": True,
            "downloads": downloads
        }

    except Exception as e:
        print(f"Error fetching downloads: {e}")
        return {
                    "success": False,
                    "downloads": []
                }

