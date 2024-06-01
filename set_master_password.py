from auth import *

def save_master_password(password):
    hashed_password = hash_password(password)
    with open('./pwds/master_pwd.key', 'wb') as f:
        f.write(hashed_password)
    print("Master password hashed and saved successfully!")
  
def set_master_password():
    while True:
        password = input("Enter the master password for your Password Manager: ")
        if check_password_strength(password):
            save_master_password(password)
            break
    
if __name__ == '__main__':
    set_master_password()