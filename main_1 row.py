import pickle
from cryptography.fernet import Fernet
from mysql import connector

data = connector.connect(host="localhost", user="root", passwd="pswrd123", database="test")
cursor = data.cursor()
upass = ""
uname = "Admin"
app = ""
def fkey(uname, app):
    key = Fernet.generate_key()
    cursor.execute('INSERT INTO try2(ky1, uname, App) VALUES ({},"{}","{}","{}")'.format(key.decode("ascii"), uname, app))
    data.commit()
def fenc(psswrd, app, uname):
    cursor.execute('SELECT ky1 FROM try2 WHERE App = "{}" AND uname = "{}"'.format(row, app, uname))
    key = cursor.fetchone()[0]
    print(type(key))
    f = Fernet(key.encode())
    enc = f.encrypt(psswrd.encode())
    denc = enc.decode()
    print(denc, type(denc))
    cursor.execute('UPDATE try2 SET ky4 = "{}" WHERE App = "{}" AND uname = "{}"'.format(denc, app, uname))
    data.commit()
def fdec(row):
    cursor.execute("SELECT ky1 FROM try2 where id = {}".format(row))
    key = cursor.fetchone()[0]
    print(key)
    dkey = key.encode()
    f = Fernet(dkey)
    cursor.execute("SELECT ky4 FROM try2 WHERE id = {}".format(row))
    pss = cursor.fetchone()[0].encode()
    dpss = f.decrypt(pss)
    print("Password is", dpss.decode())


i = 6

fkey(i)
fenc("Hello", i)
fdec(i)
