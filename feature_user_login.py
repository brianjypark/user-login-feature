import hashlib
import sqlite3
from getpass import getpass

conn = sqlite3.connect('./users.db')
c = conn.cursor()

def setup_db():
    '''
    creates table "users" in .db file

    @param none
    @returns none
    '''
    q = '''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT);
        '''
    c.execute(q)

def drop_table():
    c.execute('''DROP TABLE users;''')

def user_count():
    '''
    Sends query to db to check for pre-existing data

    @param none
    @returns {int} returns the number of rows in table "users"
    '''
    q = '''SELECT COUNT(*) FROM users;'''
    c.execute(q)
    return c.fetchone()[0]

def check_credentials(username, password):
    '''
    Given a username & password input, applies SHA256 hash to password 
    and sends a query to check if the user exists.

    @param {string} username input to check against db
    @param {string} password input to check against db
    @returns {boolean} returns True if user exists + password matches, else False
    '''
    hash_pw = get_hash(password)
    c.execute('''SELECT * FROM users WHERE username = ? AND password = ?;''', \
             (username, hash_pw))
    return c.fetchone() is not None

def get_hash(input):
    '''
    Given a string input, calculates the SHA256 hash of the input.

    @param {string} input to be hashed
    @returns {string} returns the result of the SHA256 algorithm in hexadecimal format
    ''' 
    return hashlib.sha256(input.encode('utf-8')).hexdigest()

def add_user(username, password):
    '''
    Given a username and password, applies SHA256 hash to password and
    sends a query to add the user to the db.

    @param {string} username input to insert into db
    @param {string} password input to insert into db
    @returns {boolean} returns True if user is added, else False (username is taken)
    '''
    password = get_hash(password)

    try:
        q = '''INSERT INTO users (username, password) values (?,?);'''
        c.execute(q, (username, password))
        return True
    except sqlite3.IntegrityError:
        return False

def main():
    setup_db()

    row_num = user_count()
    print("There are currently %d number of rows in the table." % row_num)

    create_table = input("Would you like to delete the current table" \
                        "and create a new one? (y/n): ").lower().strip()
    if create_table in ['y', 'yes']:
        drop_table()
        setup_db()

    while True:
        response = input("Please choose the action you would like to perform. \
                        \nType \"register\" or \"login\" or \"quit\" ").lower().strip()
        if response == 'register':
            while True:
                username = input("Please enter the username: ").lower()
                while True:
                    pw = getpass("Please enter the password: ")
                    retype_pw = getpass("Please confirm your password: ")

                    if pw == retype_pw:
                        break
                    else:
                        print("Passwords do not match. Please try again.")

                if add_user(username, pw):
                    print(f"User has been created! Username: {username}")
                    break
                else:
                    print("Username already taken. Please try again.")
            
        elif response == 'login':
            while True:
                username = input("Please enter your username: ").strip().lower()
                pw = getpass("Please enter your password: ")

                if check_credentials(username, pw):
                    print(f"Login Success: Welcome, {username}.")
                    break
                else: 
                    print(f"Login Failed. Please try again.")
                    break

        elif response == 'quit':
            conn.commit()
            conn.close()
            exit()

        else:
            print("Please enter a valid response: ")
    
if __name__ == "__main__":
    main()
