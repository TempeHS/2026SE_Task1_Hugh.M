import sqlite3 as sql
import bcrypt

connection = sql.connect("databaseFiles/database.db")
cursor = connection.cursor()


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
    cur.execute("SELECT * FROM id7-tusers")
    con.close()
    return cur
