from auth import *

def primary_phone_setup():
    phone_number = input("Enter your phone number (with country code): ")
    _,verified = verify_phone_number(phone_number)
    if verified:
        with open('./pwds/primary_phone_number.key', 'w') as f:
            f.write(phone_number)
        print("Primary Phone number verified and stored successfully.")
        return True
    else:
        print("Primary Phone number verification failed. Please try again.")
        return False

def alternative_phone_setup():  
    alternative_phone_number = input("Enter alternative phone number (with country code): ")
    _,verified = verify_phone_number(alternative_phone_number)
    if verified:
        with open('./pwds/alternative_phone_number.key', 'w') as f:
            f.write(alternative_phone_number)
        print("alternative Phone number verified and stored successfully.")
        return True
    else:
        print("alternative Phone number verification failed. Please try again.")
        return False
    
def set_phone_numbers():
    while True:
        set_primary = primary_phone_setup()
        while set_primary:
            set_alternative = alternative_phone_setup()
            if set_alternative:
                break
        if set_primary and set_alternative:
            break
    
if __name__ == '__main__':
    set_phone_numbers()