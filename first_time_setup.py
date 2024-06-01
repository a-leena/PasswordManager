import os
from generate_keys import *
from generate_recovery_code import *
from set_master_password import *
from set_phone_numbers import *

if not os.path.exists('./pwds/master_pwd.key'):
    print("First-time setup of the Password Manager")
    print()
    set_master_password()
    print()
    set_phone_numbers()
    print()
    generate_keys()
    print()
    generate_recovery_code()
    print()
    print("Setup completed successfully!\nYou may login to use your Password Manager.")
    print()

# else:
#     print("login time")
