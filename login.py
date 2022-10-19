"""
filename: login.py
Author: Brett Lubberts
Description: File containing and functions that query the database to log
a user in, or create a new user
"""
from psycopg2.extensions import connection
from psycopg2.errors import UniqueViolation

"""
log in a user if that user exists
@param connection: the connection to the database
@param username: the users username
@param password: the users password
@return True if logging in was successful, False if user didn't exist, None if error
"""


def login_user(conn: connection, username: str, password: str) -> bool | None:
    cursr = conn.cursor()
    query = (" select * from users "
             "where username = '" + username + "' and "
             "password = '" + password + "'")

    try:
        cursr.execute(query)
        if cursr.rowcount > 0:
            update = ("update users set last_access = now() where username"
                      " = '" + username + "'")
            cursr.execute(update)
            conn.commit()
            return True
    except:
        return None

    return False


"""
create a new user and add them to the database 
@param conn: the connection to the database
@param username: the new users username
@param password: the new users password
@param fname: the new users first name
@param lname: the new users last name
@param email: the new users email
@return True if new user was created successfully, False otherwise, and an optional error specifier
"""


def create_user(conn: connection, username: str, password: str, fname: str, lname: str, email: str) -> tuple[bool, str | None]:
    cursr = conn.cursor()
    query = ("insert into users(username, password, first_name, last_name,"
             "email, creation, last_access) values ('" + username + "',"
             " '" + password + "', '" + fname + "', '" + lname + "', "
             "'" + email + "', now(), now()" + ")")

    try:
        cursr.execute(query)
        conn.commit()
        return True, None
    except UniqueViolation as e:
        return False, e.diag.constraint_name
    except:
        return False, None
