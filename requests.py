from datetime import date, datetime, timedelta
from psycopg2.errors import IntegrityError
from psycopg2.extensions import cursor
from typing import Optional, Tuple


def create_req(cur: cursor, username: str, barcode: str, date_required: str, duration: str) -> Optional[bool]:
    try:
        cur.execute(
            f"insert into tool_reqs values ('{username}', (select barcode from tools where barcode = '{barcode}' and shareable and username != '{username}' and barcode not in (select barcode from tool_reqs where borrow_status != 'Accepted' or returned_date is not null)), '{date_required}', '{duration}')")
    except IntegrityError:
        return False
    except Exception as e:
        print(type(e))
        return None

    return True


def show_req(cur: cursor, req: Tuple[str, str, date, timedelta, str, Optional[datetime], Optional[date], Optional[date]]) -> None:
    try:
        username, barcode, date_required, duration, borrow_status, last_status_change, expected_return, returned_date = req

        cur.execute(f"select username from tools where barcode = '{barcode}'")

        username_to, = cur.fetchone()

        print('-' * 50)
        print(f'{username} -> {username_to} [{barcode}]')
        print(f'Required by {date_required} for {duration}')
        print(borrow_status)
        print(
            f'Last updated: {last_status_change if last_status_change else "N/A"}')
        print(
            f'Expected return: {expected_return if expected_return else "N/A"}')
        print(f'Returned: {returned_date if returned_date else "N/A"}')
        print('-' * 50)
    except:
        print('Error showing request')


def show_reqs_given(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select * from tool_reqs where username = '{username}' order by barcode")

        reqs = cur.fetchall()

        if not reqs:
            print('You have no outgoing requests')
        else:
            print(
                f'Your outgoing requests ({len(reqs)}) [barcode ascending]:')
            for req in reqs:
                show_req(cur, req)
    except:
        return False

    return True


def show_reqs_received(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select * from tool_reqs where barcode in (select barcode from tools where username = '{username}') order by barcode")

        reqs = cur.fetchall()

        if not reqs:
            print('You have no incoming requests')
        else:
            print(
                f'Your incoming requests ({len(reqs)}) [barcode ascending]:')
            for req in reqs:
                show_req(cur, req)
    except:
        return False

    return True
