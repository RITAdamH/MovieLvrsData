# Jose
from datetime import datetime

import sql

def borrow(conn, barcode, username, date, duration):
    query = "select shareable from tools where barcode = " + barcode
    shareable = sql.read_query(conn, query)

    if shareable:
        query = "insert into tools_req values(" + username + ", " + barcode + ", " + date + ", " + duration + ", Pending, " + datetime.now() + ", " + (date+duration)
        sql.execute_query(conn, query)