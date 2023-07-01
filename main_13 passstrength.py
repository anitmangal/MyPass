from cryptography.fernet import Fernet
from mysql import connector
import sys
import re



#DEFINITIONS



def init(datauser, datapass):
    global data
    global cursor
    data = connector.connect(host="localhost", user=datauser, passwd=datapass)
    cursor = data.cursor()
    try:
        cursor.execute("CREATE DATABASE PassManager")
    except:
        cursor.execute("USE PassManager")
upass = "ok"
uname = "Admin"
app = "app 1"
appuser = "usr"
with open("data.txt", "a"):
    pass
def fkey(uname, app):
    key = Fernet.generate_key()
    cursor.execute('INSERT INTO {}(keyg, App) VALUES ("{}", "{}")'.format(uname, key.decode("ascii"), app))
    data.commit()
def crtable(uname):
    try:
        cursor.execute('CREATE TABLE {} (id integer(2) PRIMARY KEY AUTO_INCREMENT, App varchar(20) UNIQUE, AppUser varchar(20), keyg varchar(50), Password Text)'.format(uname))
        data.commit()
    except:
        pass
def fenc(psswrd, app, uname, switch, appuser, appold = None, appuserold = None):
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
        cursor.execute('UPDATE {} SET Password = "{}", AppUser = "{}" WHERE App = "{}"'.format(uname, denc, appuser, app))
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
    cursor.execute('SELECT AppUser FROM {} WHERE App = "{}"'.format(uname,app))
    appuser = cursor.fetchone()[0]
    print("\n \n \nApp Username is: ")
    sys.stderr.write(appuser)
    print("\n \n \nPassword is: ")
    sys.stderr.write(dpss.decode())
    print("\n")
def mod(uname, app, appnew, psswrd, psswrdnew, appuser, appusernew) :
    try:
        denc = fenc(psswrdnew, appnew, uname, False, appusernew, app, appuser)
        cursor.execute('UPDATE {} SET App = "{}", Password = "{}", AppUser = "{}" WHERE App = "{}"'.format(uname, appnew, denc, appuser, app))
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
    cursor.execute('DROP TABLE IF EXISTS {}'.format(uname))
    data.commit()
def delapp(uname, app):
    cursor.execute("DELETE FROM {} WHERE App = '{}'".format(uname, app))
    data.commit()
def passstr(password):
    while True:   
        if (len(password)<8):
            return False
        elif not re.search("[a-z]", password): 
            return False
        elif not re.search("[A-Z]", password): 
            return False
        elif not re.search("[0-9]", password): 
            return False
        elif not re.search("[_@$*]", password): 
            return False
        elif re.search("\s", password): 
            return False
        else: 
            return True
    


    
#PROGRAM LOOP



    
while True:
    print("\n \n \n \nWelcome to your own Password Manager.")
    try:
        fl = open("data1.txt", "r")
        lst = fl.read().split(',')
        init(lst[0], lst[1])
        fl.close()
    except:
        print("To proceed further, Password Manager requires user's MySQL Database user and password")
        fl = open("data1.txt", "w")
        datauser = input("Enter MySQL database username ")
        datapass = input("Enter MySQL database password ")
        init(datauser, datapass)
        fl.write(datauser+","+datapass)
        fl.close()
    print("What do you want to do?")
    s1 = input("Do you already have a registered username? (y/n) ")
    if s1 == "y":
        uname = input("Enter Username ")
        upass = input("Enter Password ")
        if check(uname, upass):
            print("Select action \n")
        else:
            sys.stderr.write(" Invalid username or password")
            continue
    elif s1 == "n":
        while True:
            print("\n \n \nLet\'s create a username")
            uname = input("Enter username ")
            if ucheck(uname) == True:
                upass = input("Enter password ")
                if passstr(upass):
                    pass
                else:
                    print("Enter a password with atleast 8 characters, atleast one lowercase and uppercase letter, atleast one number and atleast one special character([ _ @ $ * ])")
                    continue
                create(uname, upass)
                print("Welcome back", uname, "!")
                print("Select action \n")
                break
            else:
                continue
    else:
        print("Invalid choice")
        continue
    crtable(uname)
    while True:
        print("\n \nWelcome,", uname)
        print("\n \nWhat do you want to do?")
        print(
            """\n1. Add App username and password?
2. Retrieve App username and password?
3. Modify App, username and/or password?
4. Delete App username and password?
5. Delete Account?
6. Log out?
7. Exit app?
                Enter 1/2/3/4/5/6/7 """)
        choice = int(input())
        if choice == 1:
            app = input("Enter app name ")
            appuser = input("Enter app username ")
            pswrd = input("Enter your password on the app ")
            try:
                fenc(pswrd, app, uname, True, appuser)
            except:
                sys.stderr.write("App already exists or App name invalid")
        elif choice == 2:
            try:
                cursor.execute("SELECT App FROM {}".format(uname))
                lst = cursor.fetchall()[0]
            except:
                sys.stderr.write("No app found for registered username")
                continue
            print("Available apps")
            for i in lst:
                print(i)
            app = input("Enter app name ")
            try:
                fdec(app, uname)
            except:
                sys.stderr.write("Invalid app name")
        elif choice == 3:
            try:
                cursor.execute("SELECT App FROM {}".format(uname))
                lst = cursor.fetchall()[0]
            except:
                sys.stderr.write("No app found for registered username")
                continue
            print("Available apps")
            for i in lst:
                print(i)
            app = input("Enter App to be considered ")
            cursor.execute("SELECT AppUser FROM {} WHERE App = '{}'".format(uname, app))
            appuser = cursor.fetchone()[0]
            cursor.execute('SELECT keyg FROM {} where App = "{}"'.format(uname, app))
            key = cursor.fetchone()[0]
            dkey = key.encode()
            f = Fernet(dkey)
            cursor.execute('SELECT Password FROM {} WHERE App = "{}"'.format(uname, app))
            pss = cursor.fetchone()[0].encode()
            pswrd = f.decrypt(pss)       
            choice1 = int(input("Change 1. App  2. Password  3. App Username 4. App, Username and Password  (1/2/3/4)"))
            if choice1 == 1:
                pswrdnew = pswrd
                appusernew = appuser
                appnew = input("Enter new App name ")
                mod(uname, app, appnew, pswrd, pswrdnew, appuser, appusernew)
            elif choice1 == 2:
                appnew = app
                appusernew = appuser
                pswrdnew = input("Enter password ")
                mod(uname, app, appnew, pswrd, pswrdnew, appuser, appusernew)
            elif choice1 == 3:
                appnew = app
                pswrdnew = pswrd
                appusernew = input("Enter new App username")
                mod(uname, app, appnew, pswrd, pswrdnew, appuser, appusernew)
            elif choice1 == 4:
                appnew = input("Enter new App name ")
                appusernew = input("Enter new App username")
                pswrdnew = input("Enter password ")
                mod(uname, app, appnew, pswrd, pswrdnew, appuser, appusernew)
            else:
                sys.stderr.write("Invalid choice")
        elif choice == 4:
            delete = input("Enter app name to delete ")
            confirm = input("Are you sure you want to delete {}? (y/n) ".format(delete))
            if confirm == 'y':
                delapp(uname, delete)
                print("Deleted")
            else:
                pass
        elif choice == 5:
            confirm = input("Are you sure you want to delete {}? (y/n) ".format(uname))
            if confirm == 'y':
                fl = open("data.txt", "r+")
                lst = fl.readlines()
                for i in lst:
                    if i.split(",")[0] == uname:
                        lst.pop(lst.index(i))
                        break
                    else:
                        pass
                fl.close()
                g = open("data.txt", "w")
                g.writelines(lst)
                g.close()
                deluser(uname)
                print("Deleted")
                break
            else:
                pass
        elif choice == 6 or choice == 7:
            break
        else:
            sys.stderr.write("Invalid choice")
    if choice == 7:
        break
