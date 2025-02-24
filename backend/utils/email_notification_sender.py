import random
import os
import smtplib
import datetime as dl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from utils.auth_securityDb import set_token
from config import Config

Frontend_server = Config.FRONTEND_SERVER



# Load environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PASSWORD")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT"))


def generate_random_code(length=6):
    """
    Generates a random numeric code of the specified length.

    Args:
        length (int): Length of the code to generate. Default is 6.
    Returns:
        str: Random numeric code.
    """
    return ''.join(str(random.randint(0, 9)) for _ in range(length))


def send_codes(addr, custom_message=None, length=6):
    """
    Generates a verification code and sends it via email.

    Args:
        addr (str): Recipient's email address.
        custom_message (str): Custom message (optional). If not provided, a default message is used.
        length (int): Length of the generated random code. Default is 6.

    Raises:
        ValueError: If email credentials are missing or recipient email is invalid.
        smtplib.SMTPException: If an error occurs during email transmission.
    """
    if not EMAIL or not PASSWORD:
        raise ValueError("Email credentials are not set in the environment variables.")

    if not addr or "@" not in addr:
        raise ValueError("Invalid recipient email address.")

    random_code = generate_random_code(length)

    now = dl.datetime.now()
    default_message = (
        f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
        <h1 style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">Injustify</h1>
            <p>Dear user,</p>
            <p>Please use the following code to verify your email (<span style="font-style: italic; color: gray; font-size: 12px;">{addr}</span>):</p>
            <p style="font-size: 24px; font-weight: bold; color: #000; border: 1px solid #ccc; padding: 10px; display: inline-block; background-color: #f9f9f9;">
                {random_code}
            </p>
            <p><i>(Manually copy the code above and paste it in the verification form.)</i></p>
            <p>This code will expire in 24 hours. If you need a new code, please request one.</p>
            <p>Sent on {now.strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <p>If you did not request this code, please ignore this email.</p>
        </body>
        </html>
        """
    )

    email_message = custom_message or default_message

    try:
        message = MIMEMultipart("alternative")
        message['From'] = EMAIL
        message['To'] = addr
        message['Subject'] = "Verification Code"
        message.attach(MIMEText(email_message, "html"))

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
            connection.starttls()
            connection.login(EMAIL, PASSWORD)
            connection.sendmail(EMAIL, addr, message.as_string())

        print(f"Verification code sent to {addr}: {random_code}")
        return random_code

    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise


def send_verify_link(email, token = generate_random_code(6)):
    """
    Sends a verification link to the user's registered email address.
    """
    if not email or "@" not in email:
        raise ValueError("Invalid recipient email address.")
    
    if not token:
        raise ValueError("Invalid or missing token.")

    url = f"{Frontend_server}/verify/auth?email={email}&token={token}"
    
    now = dl.datetime.now()
    
    email_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.5; color: #333;">
        <h1 style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">Injustify</h1>
        <p>Dear user,</p>
        <p>Please click the link below to verify your email:</p>
        <a href="{url}" style="font-size: 24px; font-weight: bold; color: #000; border: 1px solid #ccc; padding: 10px; display: inline-block; background-color: #f9f9f9;">
            Verify Email
        </a>
        <p>This link will expire in 10 min time. If you need a new code, please request one.</p>
        <p>Sent on {now.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <hr>
        <p>If you did not request this code, please ignore this email.</p>
    </body>
    </html>
    """
    
    message = MIMEMultipart("alternative")
    message['From'] = EMAIL
    message['To'] = email
    message['Subject'] = "Verify your email address"
    message.attach(MIMEText(email_message, "html"))

    result= set_token(email,token)
    if  result['success']== False:
        """
        check if the email has  a set token in db and the token re
        """
        return {'success': False,"message":result['message'] }


    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:
            connection.starttls() 
            connection.login(EMAIL, PASSWORD) 
            connection.sendmail(EMAIL, email, message.as_string())  


        return {'success': True, 'message':result['message']}
        
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return False

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
