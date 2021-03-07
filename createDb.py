import sqlite3


def createDb(db_name):
    # Create Database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE credentials
            (username text,
            email text,
            password text )''')
    conn.commit()
    conn.close()
    print('Database Created Successfull')


# createDb('log.db')

def selectDb(db_name):
    # Create Database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    c.execute("SELECT * FROM credentials WHERE email='{}'".format("email"))
    conn.commit()
    conn.close()


# createDb('log.db')
# selectDb('log.db')


conn = sqlite3.connect('log.db')
c = conn.cursor()
# c.execute("insert into credentials values ('{}','{}','{}')".format(
#    'fahim', 'fahgmai', 'dljfs'))

c.execute("SELECT * FROM credentials WHERE email='{}'".format('fahgmi'))
conn.commit()
t = c.fetchall()
conn.close()
print(t)
