import random
import string

def generate_recovery_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(20))
    with open ('./pwds/recovery_code.key','wb') as f:
        # encode to convert the string to bytes
        f.write(code.encode('utf-8'))
    print(f"Your recovery code is '{code}'. Save it securely.")
    
if __name__ == '__main__' :
    generate_recovery_code()