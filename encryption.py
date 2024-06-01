from cryptography.fernet import Fernet

# Load the keys
with open ('./pwds/pwdkey.key', 'rb') as f:
    key_pwd = f.read()
with open ('./pwds/unamekey.key', 'rb') as f:
    key_uname = f.read()
    
cipher_suite_pwd = Fernet(key_pwd)
cipher_suite_uname = Fernet(key_uname)

def encrypt_password(password): 
    return cipher_suite_pwd.encrypt(password.encode()).decode()

def encrypt_username(username):
    return cipher_suite_uname.encrypt(username.encode()).decode()

def encrypt(username=None, password=None):
    if username==None and password==None:
        print("Encryption failed!")
        return None, None
    elif username==None:
        return encrypt_password(password) 
    elif password==None:
        return encrypt_username(username)
    else:
        return encrypt_username(username), encrypt_password(password)
    
     
def decrypt_password(encrypted_password):
    return cipher_suite_pwd.decrypt(encrypted_password.encode()).decode()

def decrypt_username(encrypted_username):
    return cipher_suite_uname.decrypt(encrypted_username.encode()).decode()

def decrypt(encrypted_username=None, encrypted_password=None):
    if encrypted_username==None and encrypted_password==None:
        print("Decryption failed!")
        return None, None
    elif encrypted_username==None:
        return decrypt_password(encrypted_password)
    elif encrypted_password==None:
        return decrypt_username(encrypted_username)
    else:
        return decrypt_username(encrypted_username), decrypt_password(encrypted_password)