"""
filename: login.py
Author: Brett Lubberts
Description: File containing any functions that query the database to log
a user in, or create a new user
"""

from bcrypt import checkpw, gensalt, hashpw
from psycopg2.errors import IntegrityError
from psycopg2.extensions import cursor
from typing import Optional


"""
log in a user if that user exists
@param cur: the cursor to the database
@param username: the users username
@param password: the users password
@return True if logging in was successful, False if credentials were incorrect, None if error
"""


def login_user(cur: cursor, username: str, password: str) -> Optional[bool]:
    try:
        cur.execute(
            f"select password_hash from users where username = '{username}'")

        password_hash, = cur.fetchone()

        if password_hash is None or not checkpw(password.encode(), password_hash.encode()):
            return False

        cur.execute(
            f"update users set last_access = current_timestamp where username = '{username}'")
    except:
        return None

    return True


"""
create a new user and add them to the database
@param cur: the cursor to the database
@param username: the new users username
@param password: the new users password
@param fname: the new users first name
@param lname: the new users last name
@param email: the new users email
@return None if an error occurred, otherwise whether the new user was created
"""


def create_user(cur: cursor, username: str, password: str, fname: str, lname: str, email: str) -> Optional[bool]:
    try:
        cur.execute(
            f"insert into users values ('{username}', '{hashpw(password.encode(), gensalt()).decode()}', '{fname}', '{lname}', '{email}')")
    except IntegrityError:
        return False
    except Exception as e:
        print(e)
        return None

    return True
