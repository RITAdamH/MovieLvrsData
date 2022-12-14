"""
filename: tools.py
Author: Patrick Johnson
Description: File containing any functions that query the database to interact with tools
"""


from datetime import datetime
from typing_extensions import Unpack
from psycopg2.extensions import cursor
from typing import List, Optional, Tuple

from constants import TOOL

"""
add tool
@param cur: the cursor to the database
@param username: the users username
@param barcode: the barcode of the tool
@return True if execution successful, False if integrity error (user error), None if other error
"""


def add_tool(cur: cursor, username: str, barcode: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update tools set username = '{username}' where barcode = '{barcode}' and username is null")
    except:
        return None

    return cur.rowcount > 0


"""
edit tool
@param cur: the cursor to the database
@param username: the users username
@param barcode: the barcode of the tool
@param shareable: whether the tool is shareable or not
@return True if execution successful, False if integrity error (user error), None if other error
"""


def edit_tool(cur: cursor, username: str, barcode: str, shareable: bool) -> Optional[bool]:
    try:
        cur.execute(
            f"update tools set shareable = {shareable} where username = '{username}' and barcode = '{barcode}'")
    except:
        return None

    return cur.rowcount > 0


"""
remove tool
@param cur: the cursor to the database
@param username: the users username
@param barcode: the barcode of the tool
@return True if execution successful, False if integrity error (user error), None if other error
"""


def remove_tool(cur: cursor, username: str, barcode: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update tools set username = null and shareable = true from tool_reqs where tools.username = '{username}' and tools.barcode = '{barcode}' and (tool_reqs.status != 'Accepted' or tool_reqs.date_returned is not null)")

        if cur.rowcount == 0:
            return False

        cur.execute(
            f"delete from tool_categs where barcode = '{barcode}' and cid in (select cid from categories where "
            f"username = '{username}')")
        cur.execute(f"delete from tool_reqs where barcode = '{barcode}'")
    except:
        return None

    return True


"""
return tool
@param cur: the cursor to the database
@param username: the users username
@param barcode: the barcode of the tool
@return True if execution successful, False if integrity error (user error), None if other error
"""


def return_tool(cur: cursor, username: str, barcode: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update tool_reqs set date_returned = current_date where barcode = '{barcode}' and username = '{username}' and status = 'Accepted' and date_returned is null")
    except:
        return None

    return cur.rowcount > 0


"""
shows similar tools to the one borrowed
@param cur: the cursor to the database
@param username: the users username
@param tools_similar_borrows the tools that are similar to the one borrowed
"""


def show_also_borrowed(cur: cursor, username: str, tools_similar_borrows: List[Tuple[Unpack[TOOL], int]]) -> None:
    if tools_similar_borrows:
        print(
            f'People also borrowed:')
        for tool_similar_borrows in tools_similar_borrows:
            *tool, _ = tool_similar_borrows
            show_tool(cur, username, tool)


"""
show tool
@param cur: the cursor to the database
@param username: the users username
@param tool: the tool to be shown
@param show_categs: whether to show the categories a tool belongs to (default True)
@param tab: whether to print information tabbed over (default False)
@return None (if successful prints result)
"""


def show_tool(cur: cursor, username: str, tool: TOOL, show_categs: bool = True, tab: bool = False) -> None:
    try:
        barcode, name, description, purchase_date, purchase_price, shareable, tool_username = tool

        owned = tool_username == username

        start = '\t' if tab else ''

        print(start + '-' * 50)

        print(start + f'{name} [{barcode}]')

        if description is not None:
            print(start + f'"{description}"')

        if tool_username is not None:
            if owned:
                print(start + 'Owned by you')
                if purchase_date is not None and purchase_price is not None:
                    print(
                        start + f'Purchased on {purchase_date:%B %d, %Y} (${purchase_price:,.2f})')
                elif purchase_date is not None:
                    print(start + f'Purchased on {purchase_date:%B %d, %Y}')
                elif purchase_price is not None:
                    print(start + f'${purchase_price:,.2f}')
            else:
                print(start + f'Owned by {tool_username}')

            print(start + f'{"Shareable" if shareable else "Not shareable"}')
        else:
            print(start + f'Not owned')

        if owned and show_categs:
            cur.execute(
                f"select name from categories where username = '{username}' and cid in (select cid from tool_categs where barcode = '{barcode}') "
                f"order by name")

            categs = cur.fetchall()

            if categs:
                print(
                    start + f'Categories: {", ".join(name for name, in categs)}')

        cur.execute(
            f"select tool_reqs.username, tool_reqs.last_status_change, tool_reqs.expected_return_date from tool_reqs, "
            f"tools where tool_reqs.barcode = tools.barcode and tool_reqs.barcode = '{barcode}' and ("
            f"tool_reqs.username = '{username}' or tools.username = '{username}') and tool_reqs.status = 'Accepted' "
            f"and tool_reqs.date_returned is null")

        borrows = cur.fetchone()

        if borrows is not None:
            borrow_username, borrow_date, expected_return_date = borrows

            if borrow_username == username:
                print(
                    start + f'Borrowing from {tool_username} since {borrow_date:%B %d, %Y} (expected back {expected_return_date:%B %d, %Y})')
            else:
                print(
                    start + f'Borrowed by {borrow_username} since {borrow_date:%B %d, %Y} (expected back {expected_return_date:%B %d, %Y})')

            if datetime.now().date() > expected_return_date:
                print(start + 'OVERDUE')

        print(start + '-' * 50)
    except:
        print('Error showing tool')


"""
show available tools
@param cur: the cursor to the database
@param username: the users username
@return True if execution successful, False if integrity error (user error)
"""


def show_tools_available(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select * from tools where shareable and username != '{username}' and barcode not in (select barcode "
            f"from tool_reqs where status != 'Accepted' or date_returned is not null) order by name, barcode")

        tools = cur.fetchall()

        if not tools:
            print('No tools available')
        else:
            print(f'Available tools ({len(tools)}) [name ascending]:')
            for tool in tools:
                show_tool(cur, username, tool)
    except:
        return False

    return True


"""
show borrowed tools
@param cur: the cursor to the database
@param username: the users username
@return True if execution successful, False if integrity error (user error)
"""


def show_tools_borrowed(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select tools.* from tools, tool_reqs where tools.barcode = tool_reqs.barcode and tool_reqs.username = '{username}' and tool_reqs.status = 'Accepted' and tool_reqs.date_returned is null order by tool_reqs.last_status_change, tools.name, tools.barcode")

        tools = cur.fetchall()

        if not tools:
            print('You have no borrowed tools')
        else:
            print(
                f'Your borrowed tools ({len(tools)}) [lend date ascending]:')
            for tool in tools:
                show_tool(cur, username, tool)
    except:
        return False

    return True


"""
show lent tools
@param cur: the cursor to the database
@param username: the users username
@return True if execution successful, False if integrity error (user error)
"""


def show_tools_lent(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select tools.* from tools, tool_reqs where tools.barcode = tool_reqs.barcode and tools.username = '{username}' and tool_reqs.status = 'Accepted' and tool_reqs.date_returned is null order by tool_reqs.last_status_change, tools.name, tools.barcode")

        tools = cur.fetchall()

        if not tools:
            print('You have no lent tools')
        else:
            print(f'Your lent tools ({len(tools)}) [lend date ascending]:')
            for tool in tools:
                show_tool(cur, username, tool)
    except:
        return False

    return True


"""
show owned tools
@param cur: the cursor to the database
@param username: the users username
@param by: the attribute in which to order the tools
@param ord: the type of ordering (default descending)
@return True if execution successful, False if integrity error (user error)
"""


def show_tools_owned(cur: cursor, username: str, by: str, ord: str) -> bool:
    try:
        if by == 'n':
            cur.execute(
                f"select * from tools where username = '{username}' order by name {'asc' if ord == 'a' else 'desc'}, barcode")
        else:
            cur.execute(
                f"select * from tools where username = '{username}' order by (select min(name) from categories where "
                f"username = '{username}' and cid in (select cid from tool_categs where barcode = tools.barcode)) "
                f"{'asc' if ord == 'a' else 'desc'} nulls last, name, barcode")

        tools = cur.fetchall()

        if not tools:
            print('You have no tools')
        else:
            print(
                f'Your tools ({len(tools)}) [{"category" if by == "c" else "name"} {"ascending" if ord == "a" else "descending"}]:')
            for tool in tools:
                show_tool(cur, username, tool)
    except:
        return False

    return True
