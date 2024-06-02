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
        print(f"Exception occured while creating table!\n{e}")
        return False


# Add passwords to the table
def add_credentials(conn, service, username, password, is_critical):
    try:    
        encrypted_username, encrypted_password = encrypt(username,password)
        c = conn.cursor()
        c.execute('INSERT INTO passwords (service, username, password, is_critical) VALUES (?,?,?,?)', (service,encrypted_username,encrypted_password,is_critical))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occured while adding new credentials!\n{e}")
        return False

# Fetch username and password from the database for a particular service
def get_credentials(conn, service, critical_only=None):
    try:
        c = conn.cursor()
        if critical_only:
            c.execute('SELECT username,password FROM passwords WHERE service=? AND is_critical=1',(service,))
        else:
            c.execute('SELECT username,password FROM passwords WHERE service=?',(service,))
        result = c.fetchone()
        if result:
            encrypted_username, encrypted_password = result
            username, password = decrypt(encrypted_username,encrypted_password)
            return username, password
        else:
            return None, None
    except Exception as e:
        print(f"Exception occured while retrieving credentials!\n{e}")
        return None, None


# Delete the username and password for a particular service
def delete_service(conn, service):
    try:
        c = conn.cursor()
        c.execute('DELETE FROM passwords WHERE service=?',(service,))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occured while deleting credentials!\n{e}")
        return False

  
# Modify service name and/or username and/or password for a particular service
def update_service(conn, old_service_name, new_service_name):
    try:    
        c = conn.cursor()
        c.execute('UPDATE passwords SET service=? WHERE service=?', (new_service_name,old_service_name))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occured while updating credentials!\n{e}")
        return False

def update_username(conn, service, new_username):
    try:
        encrypted_username = encrypt(username=new_username)
        c = conn.cursor()
        c.execute('UPDATE passwords SET username=? WHERE service=?', (encrypted_username,service))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occured while updating credentials!\n{e}")
        return False

def update_password(conn, service, new_password):
    try:    
        encrypted_password = encrypt(password=new_password)
        c = conn.cursor()
        c.execute('UPDATE passwords SET password=? WHERE service=?',(encrypted_password,service))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occured while updating credentials!\n{e}")
        return False

def update_critical_status(conn, service, new_is_critical):
    try:
        c = conn.cursor()
        c.execute('UPDATE passwords SET is_critical=? WHERE service=?',(new_is_critical,service))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occured while updating credentials!\n{e}")
        return False

def update_all(conn, old_service_name, new_service_name, new_username, new_password, new_is_critical):
    try:
        c = conn.cursor()
        c.execute('UPDATE passwords SET service=?, username=?, password=?, is_critical=? WHERE service=?',(new_service_name,new_username,new_password,new_is_critical,old_service_name))
        conn.commit()
        return True
    except Exception as e:
        print(f"Exception occured while updating credentials!\n{e}")
        return False


# Search all usernames and service names of related services
def search_services(conn, search_term):
    try:
        c = conn.cursor()
        c.execute('SELECT service, username FROM passwords WHERE service LIKE ?', ('%' + search_term + '%',))
        results = c.fetchall()
        return_results = []
        for service_name, username in results:
            return_results.append((service_name, decrypt(encrypted_username=username)))
        return return_results
    except Exception as e:
        print(f"Exception occured while searching for services!\n{e}")
        return None