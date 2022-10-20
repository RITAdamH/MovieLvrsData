from typing import Optional
from psycopg2.errors import IntegrityError
from psycopg2.extensions import cursor

from tools import show_tool


def add_categ_tool(cur: cursor, username: str, categ_name: str, tool_barcode: str) -> Optional[bool]:
    try:
        cur.execute(
            f"insert into tool_categs(barcode, cid) values (select barcode from tools where username = '{username}' and barcode = '{tool_barcode}', (select cid from categories where username = '{username}' and name = '{categ_name}'))")
    except IntegrityError:
        return False
    except Exception as e:
        return None

    return True


def create_categ(cur: cursor, username: str, name: str) -> Optional[bool]:
    try:
        cur.execute(
            f"insert into categories(name, username) values ('{name}', '{username}')")
    except IntegrityError:
        return False
    except:
        return None

    return True


def delete_categ(cur: cursor, username: str, name: str) -> Optional[bool]:
    try:
        cur.execute(
            f"delete from categories where username = '{username}' and name = '{name}'")
    except:
        return None

    return cur.rowcount > 0


def delete_categ_tool(cur: cursor, username: str, categ_name: str, tool_barcode: str) -> Optional[bool]:
    try:
        cur.execute(
            f"delete from tool_categs where barcode = '{tool_barcode}' and cid in (select cid from categories where username = '{username}' and name = '{categ_name}')")
    except:
        return None

    return cur.rowcount > 0


def edit_categ_name(cur: cursor, username: str, old_name: str, new_name: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update categories set name = '{new_name}' where username = '{username}' and name = '{old_name}'")
    except IntegrityError:
        return False
    except:
        return None

    return cur.rowcount > 0


def show_categs(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select * from categories where username = '{username}' order by name asc")

        categs = cur.fetchall()

        print(
            f'Your categories (name ascending):')
        for categ in categs:
            cur.execute(
                f"select * from tools where barcode in (select barcode from tool_categs where cid = {categ[0]}) order by name asc")

            tools = cur.fetchall()

            print(f'{categ[1]}:')
            if not tools:
                print('\tEmpty')
            else:
                for tool in tools:
                    show_tool(cur, username, tool, show_categs=False, tab=True)

            print()
    except:
        return False

    return True
