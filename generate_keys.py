from cryptography.fernet import Fernet

def generate_keys():
    key_pwd = Fernet.generate_key()
    key_uname = Fernet.generate_key()
    with open ('./pwds/pwdkey.key','wb') as key_file:
        key_file.write(key_pwd)
    with open ('./pwds/unamekey.key','wb') as key_file:
        key_file.write(key_uname)
    print("Encryption keys generated and saved successfully!")

if __name__ == '__main__':
    generate_keys()