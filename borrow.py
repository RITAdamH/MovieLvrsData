# Jose
from datetime import datetime

import sql

def borrow(conn, barcode, username, date, duration):
    query = "select shareable from tools where barcode = " + barcode
    shareable = sql.read_query(conn, query)

    if shareable:
        query = "insert into tools_req values(" + username + ", " + barcode + ", " + date + ", " + duration + ", Pending, " + datetime.now() + ", " + (date+duration)
        sql.execute_query(conn, query)


def manage(conn, username, flag):
    if flag == "g":
        query = "select barcode, date_required from tools_req where username = " + username
        requests = list(sql.read_query(conn, query))
        for request in requests:
            print(request)
    else:
        query = "select username, barcode, date_required from tools_req where barcode = select barcode from tools where username = " + username
        requests = list(sql.read_query(conn, query))
        for request in requests:
            print(request)