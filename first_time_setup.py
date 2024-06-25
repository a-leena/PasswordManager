import os
from generate_keys import *
from generate_recovery_code import *
from set_master_password import *
from set_phone_numbers import *

# print(len(os.listdir('./pwds/')))
if not all (file in os.listdir('./pwds/') for file in ['alternative_phone_number.key', 'altnumkey.key', 'master_pwd.key', 'primary_phone_number.key', 'prnumkey.key', 'pwdkey.key', 'recovery_code.key', 'servicekey.key', 'unamekey.key']):
    set_master_password()
    print()
    set_phone_numbers()
    print()
    generate_recovery_code()
    print()
    print("Setup completed successfully!\nYou may login to use your Password Manager.")
    print()

