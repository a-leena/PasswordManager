import sqlite3
from first_time_setup import *
from utils import *
from recovery import *
from auth import *
from db import *

# Database setup
conn = sqlite3.connect('password_manager.db')
create_table(conn)

# Load the master password
with open ('./pwds/master_pwd.key', 'rb') as f:
    master_password = f.read()
    
# Load the phone numbers
with open ('./pwds/primary_phone_number.key', 'rb') as f:
    phone_number = f.read()
with open ('./pwds/alternate_phone_number.key', 'rb') as f:
    alternate_phone_number = f.read()
    
# Load the recovery code
with open ('./pwds/recovery_code.key', 'rb') as f:
    recovery_code = f.read()
