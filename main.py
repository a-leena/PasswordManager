import sqlite3
import time
from first_time_setup import *
from utils import *
from recovery import *
from auth import *
from db import *
from getpass import getpass

# Database setup
conn = sqlite3.connect('password_manager.db')
create_table(conn)

# Load the master password
def load_master_password():
    with open ('./pwds/master_pwd.key', 'rb') as f:
        return f.read()
    
# Load the phone numbers
def load_phone_numbers():
    with open ('./pwds/primary_phone_number.key', 'r') as f1:
        phone_number = f1.read()
    with open ('./pwds/alternate_phone_number.key', 'r') as f2:
        alternate_phone_number = f2.read()
    return phone_number, alternate_phone_number
    
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

# Global variables for lockout from alternate login
MAXIMUM_ATTEMPTS_MPWD_ALT = 3
MAXIMUM_ATTEMPTS_OTP_ALT = 5
LOCKOUT_DURATION_ALT = 600      # 10 minutes
failed_attempts_mpwd_alt = 0 
lockout_start_alt = None

def check_locked(time_now):
    login_blocked = lockout_start and time_now - lockout_start < LOCKOUT_DURATION
    recovery_blocked = lockout_start_rec and time_now - lockout_start_rec <  LOCKOUT_DURATION_REC
    alternate_login_blocked = lockout_start_alt and time_now - lockout_start_alt < LOCKOUT_DURATION_ALT
    return login_blocked or recovery_blocked or alternate_login_blocked
    
def login():
    global failed_attempts_mpwd, lockout_start
    if failed_attempts_mpwd >= MAXIMUM_ATTEMPTS_MPWD:
        print("Account locked due to too many failed attempts!")
        lockout_start = time.time()
        failed_attempts_mpwd = 0
        return False
        
    if check_locked(time.time()):
        print("Account Locked! Try again later.")
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
                    print("Invalid OTP!")
                    failed_attempts_otp += 1
            else:
                failed_attempts_otp += 1
        print("Account locked due to too many failed OTP attempts!")
        lockout_start = time.time()
        return False
    else:
        failed_attempts_mpwd += 1
        print("Incorrect Password! Try again.")
        return False

def recover_account():
    global failed_attempts_code_rec, lockout_start_rec
    if failed_attempts_code_rec >= MAXIMUM_ATTEMPTS_CODE_REC:
        print("Account locked due to too many failed attempts!")
        lockout_start_rec = time.time()
        failed_attempts_code_rec = 0
        return False
    
    if check_locked(time.time()):
        print("Account Locked! Try again later.")
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
                    print("Invalid OTP!")
                    failed_attempts_otp += 1
            else:
                failed_attempts_otp += 1
        print("Account locked due to too many failed OTP attempts!")
        lockout_start_rec = time.time()
        return False
    else:
        failed_attempts_code_rec += 1
        print("Incorrect Recovery Code! Try again.")
        return False
    
def alternate_login():
    global failed_attempts_mpwd_alt, lockout_start_alt
    if failed_attempts_mpwd_alt >= MAXIMUM_ATTEMPTS_MPWD_ALT:
        print("Account locked due to too many failed attempts!")
        lockout_start_alt = time.time()
        failed_attempts_mpwd_alt = 0
        return False
    
    if check_locked(time.time()):
        print("Account Locked! Try again later.")
        return False
    
    stored_master_password = load_master_password()
    provided_master_password = getpass("Enter master password: ")
    if verify_password(stored_master_password, provided_master_password):
        _, alternate_phone_number =  load_phone_numbers()
        failed_attempts_otp = 0
        for attempt in range(MAXIMUM_ATTEMPTS_OTP_ALT):
            status, verified = verify_phone_number(alternate_phone_number)
            if status:
                if verified:
                    print("Access granted!")
                    failed_attempts_mpwd_alt = 0
                    lockout_start_alt = None
                    return True
                else:
                    print("Invalid OTP!")
                    failed_attempts_otp += 1
            else:
                failed_attempts_otp += 1
        print("Account locked due to too many failed OTP attempts!")
        lockout_start_alt = time.time()
        return False
    else:
        failed_attempts_mpwd_alt += 1
        print("Incorrect Password! Try again.")
        return False
            

def main():
    while True:
        print("\nPassword Manager\n")
        print("1. Login")
        print("2. Forgot Password? Recover Account")
        print("3. Unable to get OTP? Alternate Login")
        print("4. Generate Strong Password")
        print("5. Show Instructions")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice=='1':
            if login():
                while True:
                    print("\n1. Add Credentials")
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
                        print("Assign a name to the service whose credentials you want to save")
                        service_name = input("Enter service name: ")
                        username = input("\nEnter service username/email address: ")
                        password = input("\nEnter service password: ")
                        print("Will you be needing the credentials of this service even during Alternate Login?")
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
                            print("2. Change Alternate Phone Number")
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
                                print("\nChanging Alternate Phone Number\n")
                                stored_master_password = load_master_password()
                                provided_master_password = getpass("Enter master password: ")
                                if verify_password(stored_master_password, provided_master_password):
                                    if alternate_phone_setup():
                                        _,new_alt_ph_num = load_phone_numbers()
                                        print(f"Alternate Phone Number successfully changed from {old_alt_ph_num} to {new_alt_ph_num}!")
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
            print("\nRecover Account\n")
            if recover_account():
                if set_master_password():
                    print("Master Password successfully changed!")
                else:
                    print("Master Password could not be changed!")
        
        elif choice == '3':
            if alternate_login():
                while True:
                    print("\nAlternate Login to Password Manager")       
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
                            old_ph_num, alternate_phone_number =  load_phone_numbers()
                            status, verified = verify_phone_number(alternate_phone_number)
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
            print("\nSecure Password Generator\n")
            length = int(input("Enter the length needed for password: "))
            use_special_chars = input("Should the password include special characters?(y/n): ")
            if use_special_chars.lower()=='y':
                use_special_chars = True
            else:
                use_special_chars = False
            generated_password = generate_password(length,use_special_chars)
            if generated_password:
                print("Strong Password successfully generated!")
                print(f"Password: {generated_password}")
            else:
                print("Password generation failed! Try again.")

        elif choice == '5':
            print("\nInstructions for using your Password Manager\n")
        elif choice == '6':
            print('Exiting Password Manager...')
            break

if __name__ == '__main__':
    main()