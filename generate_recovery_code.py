import random
import string
from auth import hash_password

def generate_recovery_code():
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(20))
    with open ('./pwds/recovery_code.key','wb') as f:
        f.write(hash_password(code))
    print(f"Your recovery code is '{code}'. Save it securely.")
    
if __name__ == '__main__' :
    generate_recovery_code()