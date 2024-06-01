from encryption import *

# Create the table in database for storing passwords
def create_table(conn):
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS passwords (
                  id INTEGER PRIMARY KEY,
                  service TEXT NOT NULL,
                  username TEXT NOT NULL,
                  password TEXT NOT NULL
              )
              ''')
    conn.commit()


# Add passwords to the table
def add_credentials(conn, service, username, password):
    encrypted_username, encrypted_password = encrypt(username,password)
    c = conn.cursor()
    c.execute('INSERT INTO passwords (service, username, password) VALUES (?,?,?)', service,encrypted_username,encrypted_password)
    conn.commit()


# Fetch username and password from the database for a particular service
def get_credentials(conn, service):
    c = conn.cursor()
    c.execute('SELECT username,password FROM passwords WHERE service=?',(service,))
    result = c.fetchone()
    if result:
        encrypted_username, encrypted_password = result
        username, password = decrypt(encrypted_username,encrypted_password)
        return username, password
    else:
        return None, None


# Delete the username and password for a particular service
def delete_service(conn, service):
    c = conn.cursor()
    c.execute('DELETE FROM passwords WHERE service=?',(service,))
    conn.commit()

  
# Modify service name and/or username and/or password for a particular service
def update_service(conn, old_service_name, new_service_name):
    c = conn.cursor()
    c.execute('UPDATE passwords SET service=? WHERE service=?', (new_service_name,old_service_name))
    conn.commit()

def update_username(conn, service, new_username):
    encrypted_username = encrypt(username=new_username)
    c = conn.cursor()
    c.execute('UPDATE passwords SET username=? WHERE service=?', (encrypted_username,service))
    conn.commit()

def update_password(conn, service, new_password):
    encrypted_password = encrypt(password=new_password)
    c = conn.cursor()
    c.execute('UPDATE passwords SET password=? WHERE service=?',(encrypted_password,service))
    conn.commit()

def update_all(conn, old_service_name, new_service_name, new_username, new_password):
    delete_service(conn,old_service_name)
    add_credentials(conn,new_service_name,new_username,new_password)


# Search all usernames and service names of related services
def search_passwords(conn, search_term):
    c = conn.cursor()
    c.execute('SELECT service, username FROM passwords WHERE service LIKE ?', ('%' + search_term + '%',))
    results = c.fetchall()
    print(results)
    return results