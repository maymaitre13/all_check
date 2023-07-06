import sqlite3

db = sqlite3.connect("books-collection.db")
cursor = db.cursor()


def all_user():
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    cursor.execute("select * from user")
    results = cursor.fetchall()
    return results


def search_user(email):
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    test = 0
    cursor.execute("SELECT email FROM user WHERE email=?", (email,))
    results = cursor.fetchall()
    if len(results) > 0:
        test = 1
    tab = [results, test]
    # print(tab, " in 'db/Search_user'")
    return tab


def check_password(email):
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    test = 0
    cursor.execute("SELECT password FROM user WHERE email=?", (email,))
    results = cursor.fetchall()
    if len(results) > 0:
        test = 1
    tab = [results, test]
    return tab


def add_user(name, email, password):
    db = sqlite3.connect("users.db")
    cursor = db.cursor()
    data = all_user()
    if len(data) != 0:
        id = int(data[-1][0])
        id = id+1
    else:
        id = 1

    check = search_user(name)
    if int(check[1]) == 0:
        try:
            cursor.execute("INSERT INTO user VALUES(?,?,?,?)", (id, email, password, name))
            print("Registered 'add_user'")
            db.commit()
            return True
        except Exception as e:
            print(f"Le problem :", e)
            print("Data already exist in the database")
        else:
            pass
    else:
        return False

