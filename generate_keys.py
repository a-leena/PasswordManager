from cryptography.fernet import Fernet
import os

def generate_keys():
    while True:
        key_pwd = Fernet.generate_key()
        key_uname = Fernet.generate_key()
        key_service = Fernet.generate_key()
        key_numP = Fernet.generate_key()
        key_numA = Fernet.generate_key()
        try:
            with open ('./pwds/pwdkey.key','wb') as key_file:
                key_file.write(key_pwd)
            with open ('./pwds/unamekey.key','wb') as key_file:
                key_file.write(key_uname)
            with open ('./pwds/servicekey.key','wb') as key_file:
                key_file.write(key_service)
            with open ('./pwds/prnumkey.key','wb') as key_file:
                key_file.write(key_numP)
            with open ('./pwds/altnumkey.key','wb') as key_file:
                key_file.write(key_numA)
        except Exception as e:
            print(f"Key generation failed! {e}")
            continue
        break

if len(os.listdir('./pwds/'))!=10:
    print("First-time setup of the Password Manager")
    print()
    generate_keys()