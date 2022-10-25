"""
filename: categories.py
Author: Patrick Johnson
Description: File containing any functions that query the database to alter categories for tools
"""


from psycopg2.errors import IntegrityError
from psycopg2.extensions import cursor
from typing import Optional
from tools import show_tool


"""
add tool to category
@param cur: the cursor to the database
@param username: the users username
@param categ_name: the name of a category
@param tool_barcode: the barcode of the tool to add
@return True if execution successful, False if integrity error (user error), None if other error
"""


def add_categ_tool(cur: cursor, username: str, categ_name: str, tool_barcode: str) -> Optional[bool]:
    try:
        cur.execute(
            f"insert into tool_categs(barcode, cid) values ((select barcode from tools where username = '{username}' and barcode = '{tool_barcode}'), (select cid from categories where username = '{username}' and name = '{categ_name}'))")
    except IntegrityError:
        return False
    except:
        return None

    return True


"""
create category of tools
@param cur: the cursor to the database
@param username: the users username
@param name: the name of a new category
@return True if execution successful, False if integrity error (user error), None if other error
"""


def create_categ(cur: cursor, username: str, name: str) -> Optional[bool]:
    try:
        cur.execute(
            f"insert into categories(name, username) values ('{name}', '{username}')")
    except IntegrityError:
        return False
    except:
        return None

    return True


"""
delete category of tools
@param cur: the cursor to the database
@param username: the users username
@param name: the name of a category
@return True if execution successful, False if integrity error (user error), None if other error
"""


def delete_categ(cur: cursor, username: str, name: str) -> Optional[bool]:
    try:
        cur.execute(
            f"delete from categories where username = '{username}' and name = '{name}'")
    except:
        return None

    return cur.rowcount > 0


"""
delete a tool from a category
@param cur: the cursor to the database
@param username: the users username
@param categ_name: the name of a category
@param tool_barcode: the barcode of the tool to be deleted
@return True if execution successful, False if integrity error (user error), None if other error
"""


def delete_categ_tool(cur: cursor, username: str, categ_name: str, tool_barcode: str) -> Optional[bool]:
    try:
        cur.execute(
            f"delete from tool_categs where barcode = '{tool_barcode}' and cid in (select cid from categories where "
            f"username = '{username}' and name = '{categ_name}')")
    except:
        return None

    return cur.rowcount > 0


"""
edit the name of a category
@param cur: the cursor to the database
@param username: the users username
@param old_name: the current name of a category
@param new_name: the new name of the category
@return True if execution successful, False if integrity error (user error), None if other error
"""


def edit_categ_name(cur: cursor, username: str, old_name: str, new_name: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update categories set name = '{new_name}' where username = '{username}' and name = '{old_name}'")
    except IntegrityError:
        return False
    except:
        return None

    return cur.rowcount > 0


"""
show all categories
@param cur: the cursor to the database
@param username: the users username
@return True if execution successful (prints categories), False if error
"""


def show_categs(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select * from categories where username = '{username}' order by name")

        categs = cur.fetchall()

        if not categs:
            print('No categories found')
        else:
            print(
                f'Your categories ({len(categs)}) [name ascending]:')
            for categ in categs:
                cid, name, _ = categ

                cur.execute(
                    f"select * from tools where barcode in (select barcode from tool_categs where cid = {cid}) order "
                    f"by name")

                tools = cur.fetchall()

                print(f'{name}:')
                if not tools:
                    print('\tEmpty')
                else:
                    for tool in tools:
                        show_tool(cur, username, tool,
                                  show_categs=False, tab=True)

                print()
    except:
        return False

    return True
