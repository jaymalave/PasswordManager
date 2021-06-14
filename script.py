import sqlite3
import json
import hashlib
from cryptography.fernet import Fernet


conn = sqlite3.connect('passwords.db')
cursor = conn.cursor()

def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key

key = load_key()
fer = Fernet(key)

def add():

    acc = input("Enter the account: ")
    pw = input("Enter the password: ")

    encryptedpw = fer.encrypt(pw.encode()).decode()
    

    cursor.execute('INSERT INTO PW(ACCOUNT, PASSWORD) VALUES (?, ?)', (  acc  ,  encryptedpw   ))

    conn.commit()
    
    print("success")

def view():
    
    for row in cursor.execute('SELECT * FROM PW;'):
     account = row[0]
     password = row[1]
     decpas = fer.decrypt(password.encode()).decode()
     print(account, "|", decpas)


def close():
    conn.close()


def main():

    task = input("Press r to view the passwords and w to add a new one: ")

    if task == 'r':
        view()
    elif task == 'w':
        add()
    else:
     print("Invalid request")

    close()

masterpassword = input("Enter the master-password: ")

if hashlib.sha512(masterpassword.encode()).hexdigest() == '1a2aa16e49a1107b0dcbc36e8a7488e6e0080006caa7d20e19422d3062fe9bb361e6a3b95d9fcdff47b9f13c776fcd28acbd128ad4be69a11294cf5cbb1db0fa':
    main()
else:
    print("Invalid Credentials")