from cryptography.fernet import Fernet

# Load the keys
with open ('./pwds/pwdkey.key', 'rb') as f:
    key_pwd = f.read()
with open ('./pwds/unamekey.key', 'rb') as f:
    key_uname = f.read()
with open ('./pwds/servicekey.key', 'rb') as f:
    key_service = f.read()
with open ('./pwds/prnumkey.key', 'rb') as f:
    key_numP = f.read()
with open ('./pwds/altnumkey.key', 'rb') as f:
    key_numA = f.read()
    
cipher_suite_pwd = Fernet(key_pwd)
cipher_suite_uname = Fernet(key_uname)
cipher_suite_service = Fernet(key_service)
cipher_suite_numP = Fernet(key_numP)
cipher_suite_numA = Fernet(key_numA)

def encrypt_numbers (primNum=None, altNum=None):
    if primNum==None and altNum==None:
        print("Encryption failed!")
        return None,None
    encrPrimNum = None
    encrAltNum = None
    if primNum:
        encrPrimNum = cipher_suite_numP.encrypt(primNum.encode()).decode()
    if altNum:
        encrAltNum = cipher_suite_numA.encrypt(altNum.encode()).decode()
    return encrPrimNum, encrAltNum

def encrypt_password(password): 
    return cipher_suite_pwd.encrypt(password.encode()).decode()

def encrypt_username(username):
    return cipher_suite_uname.encrypt(username.encode()).decode()

def encrypt_service(service):
    return cipher_suite_service.encrypt(service.encode()).decode()

def encrypt(service=None, username=None, password=None):
    if service==None and username==None and password==None:
        print("Encryption failed!")
        return None,None,None
    encr_p = None
    encr_u = None
    encr_s = None
    if service:
        encr_s = encrypt_service(service)
    if username:
        encr_u = encrypt_username(username)
    if password:
        encr_p = encrypt_password(password)
    return encr_s, encr_u, encr_p


def decrypt_numbers (encrPrimNum=None, encrAltNum=None):
    if encrPrimNum==None and encrAltNum==None:
        print("Decryption failed!")
        return None, None
    primNum = None
    altNum = None
    if encrPrimNum:
        primNum = cipher_suite_numP.decrypt(encrPrimNum.encode()).decode()
    if encrAltNum:
        altNum = cipher_suite_numA.decrypt(encrAltNum.encode()).decode()
    return primNum, altNum
    
def decrypt_password(encrypted_password):
    return cipher_suite_pwd.decrypt(encrypted_password.encode()).decode()

def decrypt_username(encrypted_username):
    return cipher_suite_uname.decrypt(encrypted_username.encode()).decode()

def decrypt_service(encrypted_service):
    return cipher_suite_service.decrypt(encrypted_service.encode()).decode()

def decrypt(encrypted_service=None, encrypted_username=None, encrypted_password=None):
    if encrypted_service==None and encrypted_username==None and encrypted_password==None:
        print("Decryption failed!")
        return None, None, None
    decr_p = None
    decr_u = None
    decr_s = None
    if encrypted_service:
        decr_s = decrypt_service(encrypted_service)
    if encrypted_username:
        decr_u = decrypt_username(encrypted_username)
    if encrypted_password:
        decr_p = decrypt_password(encrypted_password) 
    return decr_s, decr_u, decr_p