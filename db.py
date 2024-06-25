from encryption import *

# Create the table in database for storing passwords
def create_table(conn):
    try:
        c = conn.cursor()
        c.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY,
                    service TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL,
                    is_critical BOOLEAN NOT NULL CHECK (is_critical IN (0,1))
                )
                ''')
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occurred while creating table!\n{e}")
        return False


# Add passwords to the table
def add_credentials(conn, service, username, password, is_critical):
    try:    
        encrypted_service, encrypted_username, encrypted_password = encrypt(service, username, password)
        c = conn.cursor()
        c.execute('INSERT INTO passwords (service, username, password, is_critical) VALUES (?,?,?,?)', (encrypted_service,encrypted_username,encrypted_password,is_critical))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occurred while adding new credentials!\n{e}")
        return False

# Fetch username and password from the database for a particular service
def get_credentials(conn, service, critical_only=None):
    try:
        c = conn.cursor()
        encrypted_service = encrypt_service(service)
        if critical_only:
            c.execute('SELECT username,password FROM passwords WHERE service=? AND is_critical=1',(encrypted_service,))
        else:
            c.execute('SELECT username,password FROM passwords WHERE service=?',(encrypted_service,))
        result = c.fetchone()
        if result:
            encr_uname, encr_pword = result
            _, username, password = decrypt(encrypted_username=encr_uname,encrypted_password=encr_pword)
            return username, password
        else:
            return None, None
    except Exception as e:
        print(f"Exception occurred while retrieving credentials!\n{e}")
        return None, None


# Delete the username and password for a particular service
def delete_service(conn, service):
    try:
        c = conn.cursor()
        encrypted_service = encrypt_service(service)
        c.execute('DELETE FROM passwords WHERE service=?',(encrypted_service,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occurred while deleting credentials!\n{e}")
        return False

  
# Modify service name and/or username and/or password for a particular service
def update_service(conn, old_service_name, new_service_name):
    try:    
        c = conn.cursor()
        encr_old_service = encrypt_service(old_service_name)
        encr_new_service = encrypt_service(new_service_name)
        c.execute('UPDATE passwords SET service=? WHERE service=?', (encr_new_service,encr_old_service))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occurred while updating credentials!\n{e}")
        return False

def update_username(conn, service, new_username):
    try:
        ecnrypted_service, encrypted_username, _ = encrypt(service=service, username=new_username)
        c = conn.cursor()
        c.execute('UPDATE passwords SET username=? WHERE service=?', (encrypted_username,ecnrypted_service))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occurred while updating credentials!\n{e}")
        return False

def update_password(conn, service, new_password):
    try:    
        ecnrypted_service, _, encrypted_password = encrypt(service=service, password=new_password)
        c = conn.cursor()
        c.execute('UPDATE passwords SET password=? WHERE service=?',(encrypted_password,ecnrypted_service))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occurred while updating credentials!\n{e}")
        return False

def update_critical_status(conn, service, new_is_critical):
    try:
        c = conn.cursor()
        encrypted_service = encrypt_service(service)
        c.execute('UPDATE passwords SET is_critical=? WHERE service=?',(new_is_critical,encrypted_service))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occurred while updating credentials!\n{e}")
        return False

def update_all(conn, old_service_name, new_service_name, new_username, new_password, new_is_critical):
    try:
        c = conn.cursor()
        old_encr_service = encrypt_service(old_service_name)
        encrypted_service, encrypted_username, encrypted_password = encrypt(service=new_service_name, username=new_username, password=new_password)
        c.execute('UPDATE passwords SET service=?, username=?, password=?, is_critical=? WHERE service=?',(encrypted_service,encrypted_username,encrypted_password,new_is_critical,old_encr_service))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occurred while updating credentials!\n{e}")
        return False


# Search all usernames and service names of related services
def search_services(conn, search_term):
    try:
        c = conn.cursor()
        c.execute('SELECT service, username FROM passwords')
        results = c.fetchall()
        return_results = []
        for encr_service_name, encr_username in results:
            service = decrypt_service(encr_service_name)
            uname = decrypt_username(encr_username)
            if search_term in service:
                return_results.append((service,uname))
        return return_results
    except Exception as e:
        print(f"Exception occurred while searching for services!\n{e}")
        return None