import bcrypt
import re
import os
from twilio.rest import Client
import time
from datetime import datetime

def hash_password (password):
    salt = bcrypt.gensalt()
    pwdhash = bcrypt.hashpw(password.encode('utf-8'),salt)
    return pwdhash

def verify_password (stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)


def check_password_strength (password):
    if len(password) < 12:
        print("Password must contain at least 12 characters")
        return False
    if not re.search("[a-z]",password):
        print("Password must contain at least one lower-cased alphabet")
        return False
    if not re.search("[A-Z]",password):
        print("Password must contain at least one upper-cased alphabet")
        return False
    if not re.search("[0-9]",password):
        print("Password must contain at least one digit")
        return False
    if not re.search("[@#$%Z^_\*\-]",password):
        print("Password must contain at least one special character")
        return False
    print("Strong Password created successfully!")
    return True
        
  
# Function to send otp to user during login
def send_otp (phone_number):
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    sms_sid = os.environ['SMS_SERVICE_SID']
    client = Client(account_sid,auth_token)
    verification = client.verify.services(sms_sid)
    verification.verifications.create(to=phone_number,channel='sms')
    print(f'Sent OTP to {phone_number}')
    return verification


def verify_phone_number (phone_number):
    status = None
    verification = send_otp(phone_number)
    start_time = time.time()
    local_time = datetime.fromtimestamp(start_time+60)
    formatted_local_time = local_time.strftime('%H:%M:%S')
    print(f"(OTP expires in 1 minute. Enter OTP before {formatted_local_time})")
    provided_code = input("Enter the OTP sent to your phone: ")
    end_time = time.time()
    if end_time - start_time < 60:
        verification_check = verification.verification_checks.create(to=phone_number,code=provided_code)
        status = verification_check.status
        return status,status=='approved'
    else:
        print("OTP verification timed out.")
        return status,False