from auth import *
from getpass import getpass

def save_master_password(password):
    hashed_password = hash_password(password)
    with open('./pwds/master_pwd.key', 'wb') as f:
        f.write(hashed_password)
    print("Master password hashed and saved successfully!")
  
def set_master_password():
    while True:
        password = getpass("Enter master password for your Password Manager: ")
        confirm_password = getpass("Confirm master password for your Password Manager: ")
        if confirm_password == password:
            if check_password_strength(password):
                save_master_password(password)
                break
        else:
            print("Password didn't match! Try again.")
            
def reset_master_password():
    password = getpass("Enter master password for your Password Manager: ")
    confirm_password = getpass("Confirm master password for your Password Manager: ")
    if confirm_password == password:
        if check_password_strength(password):
            save_master_password(password)
            return True
    else:
        print("Password didn't match! Try again.")
        return False
    
if __name__ == '__main__':
    set_master_password()