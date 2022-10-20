# Jose
from datetime import datetime
from cursor import cursor
def borrow(cur: cursor, barcode, username: str, date: datetime, duration: int):
    try:
        cur.execute("select shareable from tools where barcode = " + barcode)
        shareable = cur.fetchall
        if shareable:
            cur.execute("insert into tools_req values(" + username + ", " + barcode + ", " + date + ", " + duration + ", Pending, " + datetime.now() + ", " + (
                        date + duration))
    except:
        return None
def manage(cur: cursor, username: str, flag: str):
    try:
        if flag == "g":
            cur.execute("select barcode, date_required from tools_req where username = " + username)
            requests = list(cur.fetchall)
            for request in requests:
                print(request)
        else:
            cur.execute("select username, barcode, date_required from tools_req where barcode = select barcode from tools where username = " + username)
            requests = list(cur.fetchall)
            for request in requests:
                print(request)
    except:
        return None
# requester's username
def accept(cur: cursor, username: str):
    try:
        cur.execute("update tools_req set borrow_status = Accepted, last_status_change = " + datetime.now() + " where username = " + username)
    except:
        return None
def reject(cur: cursor, username: str):
    try:
        cur.execute("update tools_req set borrow_status = Rejected, last_status_change = " + datetime.now() + " where username = " + username)
    except:
        return None
def return_tool(cur: cursor, username: str):
    print("stub")
def list_lent(cur: cursor, username: str):
    print("stub")

def list_borrowed(cur: cursor, username: str):
    print("stub")