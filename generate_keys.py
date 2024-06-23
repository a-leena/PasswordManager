from cryptography.fernet import Fernet

def generate_keys():
    while True:
        key_pwd = Fernet.generate_key()
        key_uname = Fernet.generate_key()
        try:
            with open ('./pwds/pwdkey.key','wb') as key_file:
                key_file.write(key_pwd)
        except Exception as e:
            print(f"Password Key generation failed! {e}")
            continue
        try:
            with open ('./pwds/unamekey.key','wb') as key_file:
                key_file.write(key_uname)
        except Exception as e:
            print(f"Username Key generation failed! {e}")
            continue
        print("Encryption keys generated and saved successfully!")
        break

if __name__ == '__main__':
    generate_keys()