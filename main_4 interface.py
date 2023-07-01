import pickle
from cryptography.fernet import Fernet
from mysql import connector
import sys

data = connector.connect(host="localhost", user="root", passwd="pswrd123", database="test")
cursor = data.cursor()
upass = "ok"
uname = "Admin"
app = "app 1"
def fkey(uname, app):
    key = Fernet.generate_key()
    cursor.execute('INSERT INTO try2(ky1, uname, App) VALUES ("{}","{}","{}")'.format(key.decode("ascii"), uname, app))
    data.commit()
def fenc(psswrd, app, uname):
    cursor.execute('SELECT ky1 FROM try2 WHERE App = "{}" AND uname = "{}"'.format(app, uname))
    key = cursor.fetchone()[0]
    f = Fernet(key.encode())
    enc = f.encrypt(psswrd.encode())
    denc = enc.decode()
    cursor.execute('UPDATE try2 SET ky4 = "{}" WHERE App = "{}" AND uname = "{}"'.format(denc, app, uname))
    data.commit()
def fdec(app, uname):
    cursor.execute('SELECT ky1 FROM try2 where App = "{}" and uname = "{}"'.format(app, uname))
    key = cursor.fetchone()[0]
    dkey = key.encode()
    f = Fernet(dkey)
    cursor.execute('SELECT ky4 FROM try2 WHERE App = "{}" AND uname = "{}"'.format(app, uname))
    pss = cursor.fetchone()[0].encode()
    dpss = f.decrypt(pss)
    print("Password is", dpss.decode())
def create(uname, upass):
    with open("data.txt", "a+") as fl:
        fl.write("{}, {} \n".format(uname, upass))
def check(uname, upass):
    with open("data.txt", "r") as fl:
        lst = fl.readlines()
        for i in lst:
            lstel = i.split(',')
            lstel[1] = lstel[1].rstrip().lstrip()
            if lstel[0] == uname:
                if lstel[1] == upass:
                    return True
                else:
                    return False
            else:
                return False
def ucheck(uname):
    with open("data.txt", "w+") as fl:
        lst = fl.readlines()
        for i in lst:
            lstel = i.split(',')
            if uname == lstel[0]:
                print("Username already taken")
                return False
            else:
                return True
        else:
            return True
def dele():
    cursor.execute('DELETE FROM try2')
    data.commit()
    
"""create(uname, upass)
check(uname, upass)
fkey(uname, app)
fenc("Hello", app, uname)
fdec(app, uname)
dele()"""

while True:
    print("Welcome to your own Password Manager.")
    print("What do you want to do?")
    s1 = input("Do you already have a registered username? (y/n) ")
    if s1 == "y":
        uname = input("Enter Username ")
        upass = input("Enter Password ")
        if check(uname, upass):
            print(" Select action ")
        else:
            sys.stderr.write(" Invalid username or password")
            continue
    else:
        while True:
            print("Let\'s create a username")
            uname = input("Enter username ")
            if ucheck(uname):
                upass = input("Enter password ")
                create(uname, upass)
                break
            else:
                continue
        
