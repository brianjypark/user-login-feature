import hashlib
import sqlite3
from getpass import getpass

# import json
# import os

conn = sqlite3.connect('./users.db')
c = conn.cursor()

def setup_db():
    q = '''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    );'''
    c.execute(q)

def drop_table():
    c.execute('''DROP TABLE users;''')

def user_count():
    q = '''SELECT COUNT(*) FROM users;'''
    c.execute(q)
    return c.fetchone()[0]

def check_credentials(username, password):
    password = get_hash(password)
    c.execute('''SELECT * FROM users WHERE username = ? AND password = ?;''', (username, password))
    return c.fetchone() is not None

def get_hash(input): 
    return hashlib.sha256(input.encode('utf-8')).hexdigest()

def add_user(username, password):
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

    create_table = input("Would you like to delete the current table and create a new one? (y/n): ").lower().strip()
    if create_table in ['y', 'yes']:
        drop_table()
        setup_db()

    while True:
        response = input("Please choose the action you would like to perform.\nType \"register\" | \"login\" | \"quit\" ").lower().strip()
        if response == 'register':
            while True:
                username = input("Please enter the username you would like to create: ").lower()
                while True:
                    pw = getpass("Please enter the password you would like to use: ")
                    retype_pw = getpass("Please confirm your password: ")

                    if pw == retype_pw:
                        break
                    else:
                        print("Passwords do not match. Please try again.")

                if add_user(username, pw):
                    print(f"User has been created! Username: {username}")
                    break
                else:
                    print("Username already taken, please enter a different username.")
            
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
