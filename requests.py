"""
filename: categories.py
Author: Patrick Johnson
Description: File containing any functions that query the database to request tools or related
"""


from psycopg2.errors import IntegrityError
from psycopg2.extensions import cursor
from typing import List, Optional, Tuple

from constants import TOOL_REQUEST


"""
accept tool request
@param cur: the cursor to the database
@param username: the users username
@param req_username: the username of the user who made the request
@param barcode: the barcode of the tool
@param request_date: the date the request was made
@param expected_return_date: the date the tool is expected to be returned
@return True if execution successful, False if integrity error (user error), None if other error
"""


def accept_req(cur: cursor, username: str, req_username: str, barcode: str, request_date: str, expected_return_date: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update tool_reqs set status = 'Accepted', last_status_change = current_date, expected_return_date = '{expected_return_date}' where username = '{req_username}' and barcode = '{barcode}' and request_date = '{request_date}' and status = 'Pending' and barcode in (select barcode from tools where username = '{username}' and shareable)")
    except IntegrityError:
        return False
    except:
        return None

    return cur.rowcount > 0


"""
create tool request
@param cur: the cursor to the database
@param username: the users username
@param date_returned: the date the tool was returned
@param duration: the duration of the tool
@return a tuple with True if execution successful, False if integrity error (user error), None if other error and an optional list of tools with similar borrows
"""


def create_req(cur: cursor, username: str, barcode: str, date_required: str, duration: str) -> Tuple[Optional[bool], Optional[List[tuple]]]:
    try:
        cur.execute(
            f"select tools.*, count(*) as similar_borrows from tools, tool_reqs where tools.barcode = tool_reqs.barcode and tools.barcode != '{barcode}' and (tool_reqs.username, tool_reqs.request_date) in (select username, request_date from tool_reqs where barcode = '{barcode}') group by tools.barcode order by similar_borrows desc, name, barcode limit 3")

        tools_similar_borrows = cur.fetchall()

        cur.execute(
            f"insert into tool_reqs (username, barcode, date_required, duration) values ('{username}', (select "
            f"barcode from tools where barcode = '{barcode}' and shareable and username != '{username}' and username "
            f"is not null and barcode in (select barcode from tool_reqs where status != 'Accepted' or "
            f"date_returned is not null)), '{date_required}', '{duration}')")
    except IntegrityError:
        return False, None
    except:
        return None, None

    return True, tools_similar_borrows


"""
delete tool request
@param cur: the cursor to the database
@param username: the users username
@param barcode: the barcode of the tool
@param request_date: the date the request was made
@return True if execution successful, False if integrity error (user error), None if other error
"""


def delete_req(cur: cursor, username: str, barcode: str, request_date: str) -> Optional[bool]:
    try:
        cur.execute(
            f"delete from tool_reqs where username = '{username}' and barcode = '{barcode}' and request_date = '{request_date}' and status = 'Pending'")
    except:
        return None

    return cur.rowcount > 0


"""
reject tool request
@param cur: the cursor to the database
@param username: the users username
@param req_username: the username of the user who made the request
@param barcode: the barcode of the tool
@param request_date: the date the request was made
@return True if execution successful, False if integrity error (user error), None if other error
"""


def reject_req(cur: cursor, username: str, req_username: str, barcode: str, request_date: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update tool_reqs set status = 'Denied', last_status_change = current_date where username = '{req_username}' and barcode = '{barcode}' and request_date = '{request_date}' and status = 'Pending' and barcode in (select barcode from tools where username = '{username}')")
    except:
        return None

    return cur.rowcount > 0


"""
show tool request
@param cur: the cursor to the database
@param req: the request row from the database
@return True if execution successful, False if integrity error (user error), None if other error
"""


def show_req(cur: cursor, req: TOOL_REQUEST) -> None:
    try:
        username, barcode, request_date, date_required, duration, _, _, _, _ = req

        cur.execute(f"select username from tools where barcode = '{barcode}'")

        username_to, = cur.fetchone()

        print('-' * 50)
        print(f'{username} -> {username_to} [{barcode}] ({request_date})')
        print(
            f'Required by {date_required:%B %d, %Y} for {duration.days} day(s)')
        print('-' * 50)
    except:
        print('Error showing request')


"""
show requests given
@param cur: the cursor to the database
@param username: the users username
@return True if execution successful, False if integrity error (user error), None if other error
"""


def show_reqs_given(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select * from tool_reqs where username = '{username}' and status = 'Pending' order by request_date, username, barcode")

        reqs = cur.fetchall()

        if not reqs:
            print('You have no outgoing requests')
        else:
            print(
                f'Your outgoing requests ({len(reqs)}) [request date ascending]:')
            for req in reqs:
                show_req(cur, req)
    except:
        return False

    return True


"""
show requests received
@param cur: the cursor to the database
@param username: the users username
@return True if execution successful, False if integrity error (user error), None if other error
"""


def show_reqs_received(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select * from tool_reqs where barcode in (select barcode from tools where username = '{username}') and status = 'Pending' order by request_date, username, barcode")

        reqs = cur.fetchall()

        if not reqs:
            print('You have no incoming requests')
        else:
            print(
                f'Your incoming requests ({len(reqs)}) [request date ascending]:')
            for req in reqs:
                show_req(cur, req)
    except:
        return False

    return True
