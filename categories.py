from psycopg2.errors import IntegrityError
from psycopg2.extensions import cursor

from tools import show_tool


def add_categ_tool(cur: cursor, username: str, categ_name: str, tool_barcode: str) -> bool | None:
    try:
        cur.execute(
            f"select 1 from tools where barcode = '{tool_barcode}' and username = '{username}'")
        if cur.rowcount == 0:  # check if user actually owns tool
            return False

        cur.execute(
            f"insert into tool_categs(barcode, cid) values ('{tool_barcode}', (select cid from categories where name = '{categ_name}' and username = '{username}'))")
    except IntegrityError:
        return False
    except Exception as e:
        return None

    return True


def create_categ(cur: cursor, username: str, name: str) -> bool | None:
    try:
        cur.execute(
            f"insert into categories(name, username) values ('{name}', '{username}')")
    except IntegrityError:
        return False
    except:
        return None

    return True


def delete_categ(cur: cursor, username: str, name: str) -> bool | None:
    try:
        cur.execute(
            f"delete from categories where name = '{name}' and username = '{username}'")
    except:
        return None

    return cur.rowcount > 0


def delete_categ_tool(cur: cursor, username: str, categ_name: str, tool_barcode: str) -> bool | None:
    try:
        cur.execute(
            f"delete from tool_categs using categories where name = '{categ_name}' and username = '{username}' and categories.cid = tool_categs.cid and tool_categs.barcode = '{tool_barcode}'")
    except:
        return None

    return cur.rowcount > 0


def edit_categ_name(cur: cursor, username: str, old_name: str, new_name: str) -> bool | None:
    try:
        cur.execute(
            f"update categories set name = '{new_name}' where name = '{old_name}' and username = '{username}'")
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
            print(categ[1])
            print('-' * len(categ[1]))

            cur.execute(
                f"select * from tools where barcode in (select barcode from tool_categs where cid = {categ[0]}) order by name asc")

            tools = cur.fetchall()

            for tool in tools:
                show_tool(tool)

            print()
    except:
        return False

    return True
