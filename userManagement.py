import sqlite3 as sql
import bcrypt

con = sql.connect("databaseFiles/database.db")
cur = con.cursor()


# test1 = input("un ")
# test2 = input("pw ")


# cursor.execute(
#    f"SELECT * FROM user_data WHERE username = '{test1}' AND password = '{test2}'"
# )

# credentials = cursor.fetchall()


# print(credentials)

# connection.close()


# example
def getUsers():
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM user_data")
    con.close()
    return cur


def login(un, pwd):
    con = sql.connect("databaseFiles/database.db", check_same_thread=False)
    cur = con.cursor()
    cur.execute("SELECT password FROM user_data WHERE username = ?", (un,))
    pwdata = cur.fetchone()
    con.close()
    if pwdata == None:
        print("uh oh! you didnt do this correctly! :[")
        return False
    else:
        pwinput = pwd.encode("utf-8")
        pwoutput = pwdata[0]
        print("you win!! :D")
        return bcrypt.checkpw(pwinput, pwoutput)


def signup(un, pwd):
    try:
        con = sql.connect("databaseFiles/database.db", check_same_thread=False)
        cur = con.cursor()
        bytes = pwd.encode("utf-8")
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        cur.execute("INSERT INTO user_data (username, password) VALUES (?,?)")
        con.commit()
        con.close()
        return True
    except sql.IntegrityError:
        return False
