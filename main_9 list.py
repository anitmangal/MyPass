from cryptography.fernet import Fernet
from mysql import connector
import sys

data = connector.connect(host="localhost", user="root", passwd="creator*1")
cursor = data.cursor()
try:
    cursor.execute("CREATE DATABASE PassManager")
except:
    cursor.execute("USE PassManager")
upass = "ok"
uname = "Admin"
app = "app 1"
with open("data.txt", "a"):
    pass
def fkey(uname, app):
    key = Fernet.generate_key()
    cursor.execute('INSERT INTO {}(keyg, App) VALUES ("{}", "{}")'.format(uname, key.decode("ascii"), app))
    data.commit()
def crtable(uname):
    try:
        cursor.execute('CREATE TABLE {} (id integer(2) PRIMARY KEY AUTO_INCREMENT, App varchar(20) UNIQUE, keyg varchar(50), Password Text)'.format(uname))
        data.commit()
    except:
        pass
def fenc(psswrd, app, uname, switch, appold = None):
    if switch == True:
        fkey(uname, app)
        cursor.execute('SELECT keyg FROM {} WHERE App = "{}"'.format(uname, app))
    else:
        cursor.execute('SELECT keyg FROM {} WHERE App = "{}"'.format(uname, appold))
    key = cursor.fetchone()[0]
    f = Fernet(key.encode())
    enc = f.encrypt(psswrd.encode())
    denc = enc.decode('ascii')
    if switch==True:
        cursor.execute('UPDATE {} SET Password = "{}" WHERE App = "{}"'.format(uname, denc, app))
        data.commit()
        print("Password entered safely. ")
    else:
        return denc
def fdec(app, uname):
    try:
        cursor.execute('SELECT keyg FROM {} where App = "{}"'.format(uname, app))
    except:
        sys.stderr.write("You don't have this application registered to your username")
    key = cursor.fetchone()[0]
    dkey = key.encode()
    f = Fernet(dkey)
    cursor.execute('SELECT Password FROM {} WHERE App = "{}"'.format(uname, app))
    pss = cursor.fetchone()[0].encode()
    dpss = f.decrypt(pss)
    print("\n \n \nPassword is: ")
    sys.stderr.write(dpss.decode())
    print("\n")
def mod(uname, app, appnew, psswrd, psswrdnew) :
    try:
        denc = fenc(psswrdnew, appnew, uname, False, app)
        cursor.execute('UPDATE {} SET App = "{}", Password = "{}" WHERE App = "{}"'.format(uname, appnew, denc, app))
        print("Modified successfully")
    except:
        print("Invalid app name")
    data.commit()
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
def deluser(uname):
    cursor.execute('DROP {}'.format(uname))
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
                print("Welcome back", uname, "!")
                print("Select action \n")
                break
            else:
                continue
    crtable(uname)
    while True:
        print("Welcome,", uname)
        print("\n \nWhat do you want to do?")
        print(
            """\n1. Add App username and password?
2. Retrieve App username and password?
3. Modify App username and/or password?
4. Log out?
5. Exit app?
                Enter 1/2/3/4/5 """)
        choice = int(input())
        if choice == 1:
            app = input("Enter app name ")
            pswrd = input("Enter your password on the app ")
            try:
                fenc(pswrd, app, uname, True)
            except:
                sys.stderr.write("App already exists or App name invalid")
        elif choice == 2:
            cursor.execute("SELECT App FROM {}".format(uname))
            lst = cursor.fetchall()
            print("Available apps")
            for i in lst:
                print(i)
            app = input("Enter app name ")
            try:
                fdec(app, uname)
            except:
                sys.stderr.write("Invalid app name")
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
        elif choice == 4 or choice == 5:
            break
        else:
            sys.stderr.write("Invalid choice")
    if choice == 5:
        break
