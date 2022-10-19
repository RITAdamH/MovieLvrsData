"""
filename: login.py
Author: Brett Lubberts
Description: File containing and functions that query the database to log
a user in, or create a new user
"""
import psycopg2

"""
log in a user if that user exists
@param connection: the connection to the database
@param username: the users username
@param password: the users password
@return true if user exists, false if not
"""


def login_user(connection, username, password):
    cursr = connection.cursor()
    query = (" select * from users "
             "where username = '" + username + "' and "
             "password = '" + password + "'")
    result = None
    try:
        cursr.execute(query)
        result = cursr.fetchall()

    except:
        print("user reading failed")
    if result:
        update = ("update users set last_access = now() where username"
                  " = '" + username + "'")

        try:
            cursr.execute(update)
            connection.commit()
        except:
            print("user update failed")

        return True
    else:
        return False


"""
create a new user and add them to the database 
@param connection: the connection to the database
@param username: the new users username
@param password: the new users password
@param fname: the new users first name
@param lname: the new users last name
@param email: the new users email
@return true if new user created, false otherwise
"""


def create_user(connection, username, password, fname, lname, email):
    cursr = connection.cursor()
    query = ("insert into users(username, password, first_name, last_name,"
             "email, creation, last_access) values ('" + username + "',"
             " '" + password + "', '" + fname + "', '" + lname + "', "
             "'" + email + "', now(), now()" + ")")

    try:
        cursr.execute(query)
        connection.commit()
        return True, None
    except psycopg2.errors.UniqueViolation as e:
        if e.diag.constraint_name == "users_email_key":
            return False, "Email"
        return False, "Username"
    except Exception as e:
        print(e)
        return False, None
