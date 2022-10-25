from datetime import date, datetime, timedelta
from psycopg2.errors import IntegrityError
from psycopg2.extensions import cursor
from typing import Optional, Tuple


def accept_req(cur: cursor, username: str, req_username: str, barcode: str, request_date: str, expected_return_date: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update tool_reqs set status = 'Accepted', last_status_change = current_timestamp, expected_return_date = '{expected_return_date}' where username = '{req_username}' and barcode = '{barcode}' and request_date = '{request_date}' and status = 'Pending' and barcode in (select barcode from tools where username = '{username}' and shareable)")
    except IntegrityError:
        return False
    except:
        return None

    return cur.rowcount > 0


def create_req(cur: cursor, username: str, barcode: str, date_required: str, duration: str) -> Optional[bool]:
    try:
        cur.execute(
            f"insert into tool_reqs (username, barcode, date_required, duration) values ('{username}', (select barcode from tools where barcode = '{barcode}' and shareable and username != '{username}' and username is not null and barcode not in (select barcode from tool_reqs where status != 'Accepted' or date_returned is not null)), '{date_required}', '{duration}')")
    except IntegrityError:
        return False
    except:
        return None

    return True


def delete_req(cur: cursor, username: str, barcode: str, request_date: str) -> Optional[bool]:
    try:
        cur.execute(
            f"delete from tool_reqs where username = '{username}' and barcode = '{barcode}' and request_date = '{request_date}' and status = 'Pending'")
    except:
        return None

    return cur.rowcount > 0


def reject_req(cur: cursor, username: str, req_username: str, barcode: str, request_date: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update tool_reqs set status = 'Denied', last_status_change = current_timestamp where username = '{req_username}' and barcode = '{barcode}' and request_date = '{request_date}' and status = 'Pending' and barcode in (select barcode from tools where username = '{username}')")
    except:
        return None

    return cur.rowcount > 0


def show_req(cur: cursor, req: Tuple[str, str, date, timedelta, str, Optional[datetime], Optional[date], Optional[date]]) -> None:
    try:
        # TODO: add tool name
        username, barcode, request_date, date_required, duration, _, last_status_change, expected_return_date, date_returned = req

        cur.execute(f"select username from tools where barcode = '{barcode}'")

        username_to, = cur.fetchone()

        print('-' * 50)
        print(f'{username} -> {username_to} [{barcode}] ({request_date})')
        print(f'Required by {date_required} for {duration}')
        print(
            f'Last updated: {last_status_change if last_status_change else "N/A"}')
        print(
            f'Expected return: {expected_return_date if expected_return_date else "N/A"}')
        print(f'Returned: {date_returned if date_returned else "N/A"}')
        print('-' * 50)
    except:
        print('Error showing request')


def show_reqs_given(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select * from tool_reqs where username = '{username}' and status = 'Pending' order by request_date, username")

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


def show_reqs_received(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select * from tool_reqs where barcode in (select barcode from tools where username = '{username}') and status = 'Pending' order by request_date, username")

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
