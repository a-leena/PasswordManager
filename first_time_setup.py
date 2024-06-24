import os
from generate_keys import *
from generate_recovery_code import *
from set_master_password import *
from set_phone_numbers import *

# print(len(os.listdir('./pwds/')))
if len(os.listdir('./pwds/'))!=10:
    set_master_password()
    print()
    set_phone_numbers()
    print()
    generate_recovery_code()
    print()
    print("Setup completed successfully!\nYou may login to use your Password Manager.")
    print()

