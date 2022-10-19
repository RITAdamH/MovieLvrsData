from psycopg2.errors import IntegrityError
from psycopg2.extensions import connection


def add_categ_tool(conn: connection, username: str, categ_name: str, tool_barcode: str) -> bool | None:
    cursr = conn.cursor()

    try:
        cursr.execute(
            f"select 1 from tools where barcode = '{tool_barcode}' and username = '{username}'")
        if cursr.rowcount == 0:
            return False

        cursr.execute(
            f"insert into tool_categs(barcode, cid) values ('{tool_barcode}', (select cid from categories where name = '{categ_name}' and username = '{username}'))")
        conn.commit()
    except IntegrityError:
        return False
    except Exception as e:
        return None

    return True


def create_categ(conn: connection, username: str, name: str) -> bool | None:
    cursr = conn.cursor()

    try:
        cursr.execute(
            f"select 1 from categories where name = '{name}' and username = '{username}'")

        # TODO: insert error checking instead

        if cursr.rowcount > 0:
            return False

        cursr.execute(
            f"insert into categories(name, username) values ('{name}', '{username}')")
        conn.commit()
    except:
        return None

    return True


def delete_categ(conn: connection, username: str, name: str) -> bool | None:
    cursr = conn.cursor()

    try:
        cursr.execute(
            f"select 1 from categories where name = '{name}' and username = '{username}'")

        if cursr.rowcount == 0:
            return False

        cursr.execute(
            f"delete from tool_categs using categories where name = '{name}' and username = '{username}' and categories.cid = tool_categs.cid")
        cursr.execute(
            f"delete from categories where name = '{name}' and username = '{username}'")
        conn.commit()
    except:
        return None

    return True


def delete_categ_tool(conn: connection, username: str, categ_name: str, tool_barcode: str) -> bool | None:
    cursr = conn.cursor()

    try:
        cursr.execute(
            f"delete from tool_categs using categories where name = '{categ_name}' and username = '{username}' and categories.cid = tool_categs.cid and tool_categs.barcode = '{tool_barcode}'")

        if cursr.rowcount == 0:
            return False

        conn.commit()
    except:
        return None

    return True


def edit_categ_name(conn: connection, username: str, old_name: str, new_name: str) -> bool | None:
    cursr = conn.cursor()

    try:
        cursr.execute(
            f"select 1 from categories where name = '{old_name}' and username = '{username}'")

        if cursr.rowcount == 0:
            return False

        # TODO: get rid of check ^

        cursr.execute(
            f"update categories set name = '{new_name}' where name = '{old_name}' and username = '{username}'")
        conn.commit()
    except:
        return None

    return True


def show_categs(conn: connection, username: str) -> bool:
    cursr = conn.cursor()

    try:
        cursr.execute(
            f"select * from categories where username = '{username}' order by name asc")

        categs = cursr.fetchall()

        print(
            f'Your categories (name ascending):')
        for categ in categs:
            print(categ[1])
            # TODO: show all tools in categ
            print()
    except:
        return False

    return True
