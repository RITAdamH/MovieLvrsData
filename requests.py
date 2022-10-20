from psycopg2.errors import IntegrityError
from psycopg2.extensions import cursor
from typing import Optional


def create_req(cur: cursor, username: str, barcode: str, date_required: str, duration: str) -> Optional[bool]:
    try:
        cur.execute(
            f"insert into tool_reqs values ('{username}', (select barcode from tools where barcode = '{barcode}' and shareable and username != '{username}' and barcode not in (select barcode from tool_reqs where borrow_status != 'Accepted')), '{date_required}', '{duration}')")
    except IntegrityError as e:
        print(e)
        print(type(e))
        return False
    except Exception as e:
        print(e)
        print(type(e))
        return None

    return True
