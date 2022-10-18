"""
filename: login.py
Author: Brett Lubberts
Description: File containing and functions that query the database to log
a user in, or create a new user
"""

"""
log in a user if that user exists
@param connection: the connection to the database
@param username: the users username
@param password:
@return true if user exists, false if not
"""
def login_user(connection, username, password):
        cursr = connection.cursor()
        query = """
                select * from users 
                where username = """ + username + """
                and password = """ + password
        result = None
        try:
            cursr.execute(query)
            result = cursr.fetchall()
        except:
            print("user reading failed")
        if result is not None:
            return True
        else:
            return False

"""
create a new user and add them to the database 
"""
def create_user(connection, username, password, fname, lname, email):
    cursr = connection.cursor()
    query = "insert into users(username, password, first_name, last_name,"
    "email, creation_date, last_access_date) values ('" + username + "',"
    " '" + password + "', '" + fname + "', '" + lname + "', "
    "'" + email + "', now(), now()"
    try:
        cursr.execute(query)
        connection.commit()
        return True
    except:
        return False