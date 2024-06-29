import sqlite3
import time
import string
import random
from first_time_setup import *
from auth import *
from db import *
from getpass import getpass
from encryption import decrypt_numbers

# Database setup
conn = sqlite3.connect('./pwds/password_manager.db')
create_table(conn)

# Load the master password
def load_master_password():
    with open ('./pwds/master_pwd.key', 'rb') as f:
        return f.read()
    
# Load the phone numbers
def load_phone_numbers():
    with open ('./pwds/primary_phone_number.key', 'r') as f1:
        phone_number = decrypt_numbers(encrPrimNum=f1.read())[0]
    with open ('./pwds/alternative_phone_number.key', 'r') as f2:
        alternative_phone_number = decrypt_numbers(encrAltNum=f2.read())[1]
    return phone_number, alternative_phone_number
    
# Load the recovery code
def load_recovery_code():
    with open ('./pwds/recovery_code.key', 'rb') as f:
        return f.read()
    
    
# Global variables for lockout from login
MAXIMUM_ATTEMPTS_MPWD = 3
MAXIMUM_ATTEMPTS_OTP = 5
LOCKOUT_DURATION = 300      # 5 minutes
failed_attempts_mpwd = 0 
lockout_start = None

# Global variables for lockout from recovering account
MAXIMUM_ATTEMPTS_CODE_REC = 2
MAXIMUM_ATTEMPTS_OTP_REC = 3
LOCKOUT_DURATION_REC = 7200      # 2 hours
failed_attempts_code_rec = 0 
lockout_start_rec = None

# Global variables for lockout from alternative login
MAXIMUM_ATTEMPTS_MPWD_ALT = 3
MAXIMUM_ATTEMPTS_OTP_ALT = 5
LOCKOUT_DURATION_ALT = 600      # 10 minutes
failed_attempts_mpwd_alt = 0 
lockout_start_alt = None

def check_locked(time_now):
    try_after = 0
    login_blocked = lockout_start and time_now - lockout_start < LOCKOUT_DURATION
    if login_blocked:
        try_after = LOCKOUT_DURATION - (time_now - lockout_start)
    recovery_blocked = lockout_start_rec and time_now - lockout_start_rec <  LOCKOUT_DURATION_REC
    if recovery_blocked:
        try_after = LOCKOUT_DURATION_REC - (time_now - lockout_start_rec)
    alternative_login_blocked = lockout_start_alt and time_now - lockout_start_alt < LOCKOUT_DURATION_ALT
    if alternative_login_blocked:
        try_after = LOCKOUT_DURATION_ALT - (time_now - lockout_start_alt)
    return login_blocked or recovery_blocked or alternative_login_blocked, try_after
    
def locking_message():
    print("Account locked due to too many failed attempts.")

def locking_message_otp():
    print("Account locked due to too many failed OTP attempts.")

def locked_message(try_after):
    unit = "seconds" if try_after<60 else "minutes"
    print(f"\nAccount Locked! Try again after {try_after//60 if try_after>=60 else try_after} {unit}.")
    
    
def login():
    global failed_attempts_mpwd, lockout_start
    
    locked, try_after = check_locked(time.time())
    if locked:
        locked_message(try_after)
        return False
        
    stored_master_password = load_master_password()
    provided_master_password = getpass("Enter master password: ")
    if verify_password(stored_master_password, provided_master_password):
        phone_number, _ =  load_phone_numbers()
        failed_attempts_otp = 0
        for attempt in range(MAXIMUM_ATTEMPTS_OTP):
            status, verified = verify_phone_number(phone_number)
            if status:
                if verified:
                    print("Access granted!")
                    failed_attempts_mpwd = 0
                    lockout_start = None
                    return True
                else:
                    failed_attempts_otp += 1
                    print("Invalid OTP!")
                    if failed_attempts_otp < MAXIMUM_ATTEMPTS_OTP:
                        print(f"{MAXIMUM_ATTEMPTS_OTP-failed_attempts_otp} attempts left.")
            else:
                failed_attempts_otp += 1
                if failed_attempts_otp < MAXIMUM_ATTEMPTS_OTP:
                    print(f"{MAXIMUM_ATTEMPTS_OTP-failed_attempts_otp} attempts left.")
        locking_message_otp()
        lockout_start = time.time()
        return False
    else:
        failed_attempts_mpwd += 1
        print("Incorrect Password!")
        if failed_attempts_mpwd >= MAXIMUM_ATTEMPTS_MPWD:
            locking_message()
            lockout_start = time.time()
            failed_attempts_mpwd = 0
        else:
            print(f"{MAXIMUM_ATTEMPTS_MPWD-failed_attempts_mpwd} attempts left.")
        return False

def recover_account():
    global failed_attempts_code_rec, lockout_start_rec
    
    locked, try_after = check_locked(time.time())
    if locked:
        locked_message(try_after)
        return False
    
    stored_recovery_code = load_recovery_code()
    provided_recovery_code = input("Enter recovery code: ")
    if verify_password(stored_recovery_code, provided_recovery_code):
        phone_number, _ =  load_phone_numbers()
        failed_attempts_otp = 0
        for attempt in range(MAXIMUM_ATTEMPTS_OTP_REC):
            status, verified = verify_phone_number(phone_number)
            if status:
                if verified:
                    print("Access granted!")
                    failed_attempts_code_rec = 0
                    lockout_start_rec = None
                    return True
                else:
                    failed_attempts_otp += 1
                    print("Invalid OTP!")
                    if failed_attempts_otp < MAXIMUM_ATTEMPTS_OTP_REC:
                        print(f"{MAXIMUM_ATTEMPTS_OTP_REC-failed_attempts_otp} attempts left.")
            else:
                failed_attempts_otp += 1
                if failed_attempts_otp < MAXIMUM_ATTEMPTS_OTP_REC:
                    print(f"{MAXIMUM_ATTEMPTS_OTP_REC-failed_attempts_otp} attempts left.")
        locking_message_otp()
        lockout_start_rec = time.time()
        return False
    else:
        failed_attempts_code_rec += 1
        print("Incorrect Recovery Code!")
        if failed_attempts_code_rec >= MAXIMUM_ATTEMPTS_CODE_REC:
            locking_message()
            lockout_start_rec = time.time()
            failed_attempts_code_rec = 0
        else:
            print(f"{MAXIMUM_ATTEMPTS_CODE_REC-failed_attempts_code_rec} attempts left.")
        return False
    
def alternative_login():
    global failed_attempts_mpwd_alt, lockout_start_alt
    
    locked, try_after = check_locked(time.time())
    if locked:
        locked_message(try_after)
        return False
    
    stored_master_password = load_master_password()
    provided_master_password = getpass("Enter master password: ")
    if verify_password(stored_master_password, provided_master_password):
        primary_phone_number, alternative_phone_number =  load_phone_numbers()
        send_otp(primary_phone_number)
        failed_attempts_otp = 0
        for attempt in range(MAXIMUM_ATTEMPTS_OTP_ALT):
            status, verified = verify_phone_number(alternative_phone_number)
            if status:
                if verified:
                    print("Access granted!")
                    failed_attempts_mpwd_alt = 0
                    lockout_start_alt = None
                    return True
                else:
                    failed_attempts_otp += 1
                    print("Invalid OTP!")
                    if failed_attempts_otp < MAXIMUM_ATTEMPTS_OTP_ALT:
                        print(f"{MAXIMUM_ATTEMPTS_OTP_ALT-failed_attempts_otp} attempts left.")
            else:
                failed_attempts_otp += 1
                if failed_attempts_otp < MAXIMUM_ATTEMPTS_OTP_ALT:
                    print(f"{MAXIMUM_ATTEMPTS_OTP_ALT-failed_attempts_otp} attempts left.")
        locking_message_otp()
        lockout_start_alt = time.time()
        return False
    else:
        failed_attempts_mpwd_alt += 1
        print("Incorrect Password!")
        if failed_attempts_mpwd_alt >= MAXIMUM_ATTEMPTS_MPWD_ALT:
            locking_message()
            lockout_start_alt = time.time()
            failed_attempts_mpwd_alt = 0
        else:
            print(f"{MAXIMUM_ATTEMPTS_MPWD_ALT-failed_attempts_mpwd_alt} attempts left.")
        return False

def generate_password(length=12, use_special_chars=True):
    characters = string.ascii_letters + string.digits
    if use_special_chars:
        characters += "[@#$%Z^_\*\-]"
    return ''.join(random.choice(characters) for i in range(length))     

def instructions():
    print("1. For initial setup of your Password Manager-")     
    print("  a. Create a strong Master Password.")
    print("    - Password be at least 12 characters long.")
    print("    - Password must contain upper & lower-case alphabets, numerical digits and special characters.")
    print("  b. Have one primary and one alternative phone number.")
    print("    - Make sure that your primary phone number is always accessible to you for OTP verifications during Login.")
    print("  c. A recovery code will be generated.")
    print("    - You must ensure that this code is stored somewhere securely in case of forgetting your master password.")
    print("2. Login to the Password Manager.")
    print("  - Enter your master password and OTP sent to your primary phone number.")
    print("  - For each credential (pair of username/email and password), that you want to store in your Password Manager, assign a name to its service.")
    print("  - When requesting to view a credential the service name must be provided.")
    print("  - If there are many services with similar names, then the Search feature can be used. Enter the part of the name you recall and all services with names matching your query will be displayed to you along with their respective usernames. Once you have found the service-username pair you actually wanted, use that service name to retrieve the password.")
    print("3. In case you have forgotten your master password, you can Recover your Password Manager using the recovery code and an OTP will be sent to your primary phone number for verification.")
    print("4. If your primary phone number is temporarily inaccessible you may use the alternative Login method to access your Password Manager using your master password and an OTP sent to your alternative phone number.")
    print("  - You will only have limited access to your Password Manager.")
    print("  - You can only view the credentials that are highly critical for you to access.")
    print("  - Search will be disabled, you are required to remember the names you had given to the few services whose credentials are highly critical to you.")
    print("  - For the security of your credentials it is advisable to not set all of them as highly critical.")
    
def main():
    while True:
        print("\n------ PASSWORD MANAGER APP ------\n")
        print("1. Login")
        print("2. Forgot Password? Recover Account")
        print("3. Unable to get OTP on Primary Phone? Alternative Login")
        print("4. Generate Strong Password")
        print("5. Show Instructions")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice=='1':
            if login():
                while True:
                    print("\n---PASSWORD MANAGER---\n")
                    print("1. Add Credentials")
                    print("2. Retrieve Credentials")
                    print("3. Update Credentials")
                    print("4. Delete Credentials")
                    print("5. Search for Credentials")
                    print("6. Change Master Password")
                    print("7. Change Linked Phone Numbers")
                    print("8. Logout")
                    action = input("Enter your choice: ")
                    
                    if action=='1':
                        print("\nAdd New Credentials\n")
                        print("Assign a name to the service whose credentials you want to save\n(Maximum 15 characters long; Only alphabets and digits allowed)")
                        while True:
                            service_name = input("Enter service name: ")
                            if len(service_name)>15:
                                print("Service name too long!")
                                continue
                            pattern = re.compile(r'^[a-zA-Z0-9]+$')
                            if not bool(pattern.match(service_name)):
                                print("Invalid service name!")
                                continue
                            else:
                                break
                        username = input("\nEnter service username/email address: ")
                        password = input("\nEnter service password: ")
                        print("Will you be needing the credentials of this service even during Alternative Login?")
                        is_critical = input("Is the service highly critical? (y/n): ")
                        if is_critical.lower()=='y':
                            is_critical = 1
                        else:
                            is_critical = 0
                        print(f"\nConfirm the details entered - \nService Name: {service_name}\nUsername: {username}\nPassword: {password}\nIs Critical: {'YES' if is_critical else 'NO'}\n")
                        confirm = input("Continue to Save?(y/n): ")
                        if confirm.lower()=='y':
                            if add_credentials(conn,service_name,username,password,is_critical):
                                print("New Credentials successfully added!")
                    
                    elif action=='2':
                        print("\nRetrieve Credentials\n")
                        service_name = input("Enter service name: ")
                        username,password = get_credentials(conn,service_name)
                        if username and password:
                            print(f"\nUsername: {username}\nPassword: {password}")
                        else:
                            print("No credentials for this service!")
                        
                    elif action=='3':
                        while True:
                            print("\nUpdate Credentials\n")
                            print("1. Change Service Name")
                            print("2. Change Service Username")
                            print("3. Change Service Password")
                            print("4. Change Service Critical Status (is/is not critical)")
                            print("5. Change all")
                            print("6. Go back")
                            update_action = input("Enter your choice: ")
                            if update_action=='1':
                                old_service_name = input("Enter current service name: ")
                                new_service_name = input("Enter new service name:")
                                print(f"Changing service name from {old_service_name} to {new_service_name}")
                                confirm = input("Save changes?(y/n): ")
                                if confirm.lower()=='y':
                                    if update_service(conn,old_service_name,new_service_name):
                                        print("Service name successfully modified!")
                            
                            elif update_action=='2':
                                service_name = input("Enter service name: ")
                                new_username = input("Enter new username: ")
                                old_username,_ = get_credentials(conn,service_name)
                                print(f"Changing username from {old_username} to {new_username}")
                                confirm = input("Save changes?(y/n): ")
                                if confirm.lower()=='y':
                                    if update_username(conn,service_name,new_username):
                                        print("Service Username successfully modified!")
                                        
                            elif update_action=='3':
                                service_name = input("Enter service name: ")
                                new_password = input("Enter new password: ")
                                _,old_password = get_credentials(conn,service_name)
                                print(f"Changing password from {old_password} to {new_password}")
                                confirm = input("Save changes?(y/n): ")
                                if confirm.lower()=='y':
                                    if update_password(conn,service_name,new_password):
                                        print("Service Password successfully modified!")
                            
                            elif update_action=='4':
                                service_name = input("Enter service name: ")
                                new_critical_status = input("Is the service highly critical? (y/n): ")
                                if new_critical_status.lower()=='y':
                                    new_critical_status = 1
                                    print("Setting service as Critical")
                                else:
                                    new_critical_status = 0
                                    print("Setting service as Not Critical")
                                confirm = input("Save changes?(y/n): ")
                                if confirm.lower()=='y':
                                    if update_critical_status(conn,service_name,new_critical_status):
                                        print("Service Critical Status successfully modified!")
                                        
                            elif update_action=='5':
                                old_service_name = input("Enter current service name: ")
                                new_service_name = input("Enter new service name:")
                                new_username = input("Enter new username: ")
                                new_password = input("Enter new password: ")
                                new_critical_status = input("Is the service highly critical? (y/n): ")
                                old_username,old_password = get_credentials(conn,old_service_name)
                                print(f"Changing service name from {old_service_name} to {new_service_name}")
                                print(f"Changing username from {old_username} to {new_username}")
                                print(f"Changing password from {old_password} to {new_password}")
                                if new_critical_status.lower()=='y':
                                    new_critical_status = 1
                                    print("Setting service as Critical")
                                else:
                                    new_critical_status = 0
                                    print("Setting service as Not Critical")
                                confirm = input("Save changes?(y/n): ")
                                if confirm.lower()=='y':
                                    if update_all(conn,old_service_name,new_service_name,new_username,new_password,new_critical_status):
                                        print("Service Credentials successfully modified!")
                            
                            elif update_action=='6':
                                break
                            
                            else:
                                print("Invalid choice!")
                                 
                    elif action=='4':
                        print("\nDelete Credentials\n")
                        service_name = input("Enter service name: ")
                        print(f"Deleting credentials of {service_name} service")
                        confirm = input("Save changes?(y/n): ")
                        if confirm.lower()=='y':
                            if delete_service(conn,service_name):
                                print("Service Credentials successfully deleted!")
                        
                    elif action=='5':
                        print("\nSearch for Services\n")
                        search_term = input("Enter search term: ")
                        results = search_services(conn,search_term)
                        if results:
                            print("\nSearch results-\n")
                            for i in range(len(results)):
                                print(f"Service {i+1}: {results[i][0]}\nUsername: {results[i][1]}\n")
                        else:
                            print("No matching services!")
                    
                    elif action=='6':
                        print("\nChange Master Password\n")
                        stored_master_password = load_master_password()
                        provided_master_password = getpass("Enter current master password: ")
                        if verify_password(stored_master_password, provided_master_password):
                            phone_number, _ =  load_phone_numbers()
                            status, verified = verify_phone_number(phone_number)
                            if status and verified:
                                if set_master_password():
                                    print("Master Password successfully changed!")
                                else:
                                    print("Master Password could not be changed!")
                            else:
                                print("Incorrect OTP!")
                        else:
                            print("Incorrect Password!")
                            
                    elif action=='7':
                        while True:
                            print("\nChange Linked Phone Numbers\n")
                            print("1. Change Primary Phone Number")
                            print("2. Change alternative Phone Number")
                            print("3. Go back")
                            update_action = input("Enter your choice: ")
                            if update_action=='3':
                                break
                            old_ph_num, old_alt_ph_num = load_phone_numbers()
                            if update_action=='1':
                                print("\nChanging Primary Phone Number\n")
                                stored_master_password = load_master_password()
                                provided_master_password = getpass("Enter master password: ")
                                if verify_password(stored_master_password, provided_master_password):
                                    if primary_phone_setup():
                                        new_ph_num,_ = load_phone_numbers()
                                        print(f"Primary Phone Number successfully changed from {old_ph_num} to {new_ph_num}!")
                                else:
                                    print("Incorrect Password!")
                            
                            elif update_action=='2':
                                print("\nChanging Alternative Phone Number\n")
                                stored_master_password = load_master_password()
                                provided_master_password = getpass("Enter master password: ")
                                if verify_password(stored_master_password, provided_master_password):
                                    if alternative_phone_setup():
                                        _,new_alt_ph_num = load_phone_numbers()
                                        print(f"Alternative Phone Number successfully changed from {old_alt_ph_num} to {new_alt_ph_num}!")
                                else:
                                    print("Incorrect Password!")        
                            else:
                                print("Invalid choice!")
                                
                    elif action=='8':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice!")
        
        elif choice == '2':
            if recover_account():
                print("\n---PASSWORD MANAGER (RECOVERY MODE)---\n")
                if reset_master_password():
                    print("Master Password successfully changed!")
                else:
                    print("Master Password could not be changed!")
        
        elif choice == '3':
            if alternative_login():
                while True:
                    print("\n---PASSWORD MANAGER (ALTERNATIVE MODE)---\n")       
                    print("1. Retrieve Critical Credentials")
                    print("2. Change Primary Phone Number")
                    print("3. Logout")
                    action = input("Enter your choice: ")
                    if action=='1':
                        print("\nRetrieve Critical Credentials\n")
                        service_name = input("Enter service name: ")
                        username,password = get_credentials(conn,service_name,critical_only=True)
                        if username and password:
                            print(f"\nUsername: {username}\nPassword: {password}")
                        else:
                            print("No credentials for this service or service inaccessible!")
                    
                    elif action=='2':
                        print("\nChanging Primary Phone Number\n")
                        stored_master_password = load_master_password()
                        provided_master_password = getpass("Enter master password: ")
                        if verify_password(stored_master_password, provided_master_password):
                            old_ph_num, alternative_phone_number =  load_phone_numbers()
                            status, verified = verify_phone_number(alternative_phone_number)
                            if status and verified:
                                if primary_phone_setup():
                                    new_ph_num,_ = load_phone_numbers()
                                    print(f"Primary Phone Number successfully changed from {old_ph_num} to {new_ph_num}!")
                        else:
                            print("Incorrect Password!")
                        break
                    
                    elif action=='3':
                        print("Logging out...")
                        break
                    
                    else:
                        print("Invalid choice!")
        elif choice == '4':
            print("\n---STRONG PASSWORD GENERATOR---\n")
            length = int(input("Enter the length needed for password: "))
            use_special_chars = input("Should the password include special characters?(y/n): ")
            if use_special_chars.lower()=='y':
                use_special_chars = True
            else:
                use_special_chars = False
            while True:
                generated_password = generate_password(length,use_special_chars)
                if generated_password:
                    print("Strong Password successfully generated!")
                    print(f"Password: {generated_password}")
                    next_action = "3"
                    while next_action!="1" and next_action!="2":
                        print("1. Regenerate Password")
                        print("2. Exit")
                        next_action = input("Enter your choice: ")
                        if next_action == '1':
                            print()
                        elif next_action == '2':
                            print("Exiting Password Generator...")
                        else:
                            print("Invalid choice!")
                    if next_action=="2":
                        break
                else:
                    print("Password generation failed! Try again.")  
                    break 
            

        elif choice == '5':
            print("\n---INSTRUCTIONS FOR USING PASSWORD MANAGER APP---\n")
            instructions()
            
        elif choice == '6':
            print('Exiting Password Manager...')
            break

if __name__ == '__main__':
    main()