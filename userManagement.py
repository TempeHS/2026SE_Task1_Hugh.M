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
        cur.execute(
            "INSERT INTO user_data (username, password) VALUES (?,?)", (un, hash)
        )
        con.commit()
        con.close()
        return True
    except sql.IntegrityError:
        print("error")
        print(un, pwd)
        return False


def devlogpost(
    dev_name, proj_name, start_time, end_time, entry_time, working_time, repository, dev_notes
):
    try: 
        con = sql.connect("databaseFiles/devlogs.db", check_same_thread=False)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO devlogs (devname, projectname, starttime, endtime, entrytime, workingtime, repo, devnotes) VALUES (?,?,?,?,?,?,?,?)", (dev_name, proj_name, start_time, end_time, entry_time, working_time, repository, dev_notes),
        )
        con.commit()
        con.close()
    except sql.IntegrityError:
        print("integrityerror")
        return False


def searchdevlogs(searchfunc): ...
