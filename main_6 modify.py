import pickle
from cryptography.fernet import Fernet
from mysql import connector
import sys

data = connector.connect(host="localhost", user="root", passwd="pswrd123", database="test")
cursor = data.cursor()
upass = "ok"
uname = "Admin"
app = "app 1"
with open("data.txt", "a"):
    pass
def fkey(uname, app):
    key = Fernet.generate_key()
    cursor.execute('INSERT INTO try2(ky1, uname, App) VALUES ("{}","{}","{}")'.format(key.decode("ascii"), uname, app))
    data.commit()
def fenc(psswrd, app, uname, switch):
    fkey(uname, app)
    cursor.execute('SELECT ky1 FROM try2 WHERE App = "{}" AND uname = "{}"'.format(app, uname))
    key = cursor.fetchone()[0]
    f = Fernet(key.encode())
    enc = f.encrypt(psswrd.encode())
    denc = enc.decode('ascii')
    if switch==True:
        cursor.execute('UPDATE try2 SET ky4 = "{}" WHERE App = "{}" AND uname = "{}"'.format(denc, app, uname))
        data.commit()
        print("Password entered safely. ")
    else:
        return denc
def fdec(app, uname):
    try:
        cursor.execute('SELECT ky1 FROM try2 where App = "{}" and uname = "{}"'.format(app, uname))
    except:
        sys.stderr.write("You don't have any application registered to your username")
    key = cursor.fetchone()[0]
    dkey = key.encode()
    f = Fernet(dkey)
    cursor.execute('SELECT ky4 FROM try2 WHERE App = "{}" AND uname = "{}"'.format(app, uname))
    pss = cursor.fetchone()[0].encode()
    dpss = f.decrypt(pss)
    print("Password is", dpss.decode())
def mod(uname, app, appnew, psswrd, psswrdnew) :
    try:
        denc = fenc(psswrdnew, appnew, uname, False)
        cursor.execute('UPDATE try2 SET App = "{}" ky4 = "{}" WHERE App = "{}" AND uname = "{}"'.format(appnew, denc, app, uname))
        print("Modified successfully")
    except:
        sys.stderr.write("App or username not found")
def create(uname, upass):
    with open("data.txt", "a+") as fl:
        fl.write("{}, {} \n".format(uname, upass))
        data.commit()
        print("You are now a registered user. ")
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
    with open("data.txt", "r") as fl:
        lst = fl.readlines()
        for i in lst:
            lstel = i.split(',')
            if uname == lstel[0]:
                sys.stderr.write("Username already taken")
                return False
            else:
                pass
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
    print("\n \n \n \nWelcome to your own Password Manager.")
    print("What do you want to do?")
    s1 = input("Do you already have a registered username? (y/n) ")
    if s1 == "y":
        uname = input("Enter Username ")
        upass = input("Enter Password ")
        if check(uname, upass):
            print(" Select action \n")
        else:
            sys.stderr.write(" Invalid username or password")
            continue
    else:
        while True:
            print("\n \n \nLet\'s create a username")
            uname = input("Enter username ")
            if ucheck(uname) == True:
                upass = input("Enter password ")
                create(uname, upass)
                break
                print("Welcome back", uname, "!")
                print("Select action \n")
            else:
                continue
    print("\n \nWhat do you want to do?")
    print(
        """\n1. Add App username and password?
2. Retrieve App username and password?
3. Modify App username and/or password?
4. Exit?
5. Restart app?
            Enter 1/2/3/4/5 """)
    choice = int(input())
    if choice == 1:
        app = input("Enter app name ")
        pswrd = input("Enter your password on the app ")
        fenc(pswrd, app, uname, True)
    elif choice == 2:
        app = input("Enter app name ")
        fdec(app, uname)
    elif choice == 3:
        app = input("Enter old App to be considered ")
        pswrd = input("Enter old password to be considered ")        
        choice1 = int(input("Change 1. App  2. Password  3. Both? (1/2/3)"))
        if choice1 == 1:
            pswrdnew = pswrd
            appnew = input("Enter new App name ")
            mod(uname, app, appnew, pswrd, pswrdnew)
        elif choice1 == 2:
            appnew = app
            pswrdnew = input("Enter password ")
            mod(uname, app, appnew, pswrd, pswrdnew)
        elif choice1 == 3:
            appnew = input("Enter new App name ")
            pswrdnew = input("Enter password ")
            mod(uname, app, appnew, pswrd, pswrdnew)
        else:
            sys.stderr.write("Invalid choice")
    elif choice == 4:
        break
    elif choice == 5:
        continue
    else:
        sys.stderr.write("Invalid choice")
