from typing import Any, Optional, Tuple

from psycopg2.extensions import cursor


def add_tool(cur: cursor, username: str, barcode: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update tools set username = '{username}' where barcode = '{barcode}' and username is null")
    except:
        return None

    return cur.rowcount > 0


def edit_tool(cur: cursor, username: str, barcode: str, shareable: bool) -> Optional[bool]:
    try:
        cur.execute(
            f"update tools set shareable = {shareable} where username = '{username}' and barcode = '{barcode}'")
    except:
        return None

    return cur.rowcount > 0


def remove_tool(cur: cursor, username: str, barcode: str) -> Optional[bool]:
    try:
        cur.execute(
            f"update tools set username = null where username = '{username}' and barcode = '{barcode}'")

        if cur.rowcount == 0:  # tool doesn't exists or not owned by user
            return False

        cur.execute(
            f"delete from tool_categs where barcode = '{barcode}' and cid in (select cid from categories where username = '{username}')")
    except:
        return None

    return True


def show_tool(cur: cursor, username: str, tool: Tuple[Any], show_categs: bool = True, tab: bool = False) -> None:
    owned = tool[6] == username
    start = '\t' if tab else ''
    print(start + '-' * 80)
    print(start + f'{tool[1]} [{tool[0]}]')
    print(start + f'"{tool[2]}"')
    if owned:
        print(start + "Owned by you")
        print(start + f'Purchased on {tool[3]} (${tool[4]:.2f})')
    print(start + f'{"Shareable" if tool[5] else "Not shareable"}')
    if owned and show_categs:
        cur.execute(
            f"select name from categories where username = '{username}' and cid in (select cid from tool_categs where barcode = '{tool[0]}') order by name asc")

        categs = cur.fetchall()

        print(
            start + f'Categories: {", ".join([categ for categ, in categs])}')
    print(start + '-' * 80)


def show_tools(cur: cursor, username: str, by: str, ord: str) -> bool:
    try:
        if by == 'n':
            cur.execute(
                f"select * from tools where username = '{username}' order by name {'asc' if ord == 'a' else 'desc'}")
        else:
            cur.execute(
                f"select * from tools where username = '{username}' order by (select min(name) from categories where username = '{username}' and cid in (select cid from tool_categs where barcode = tools.barcode)) {'asc' if ord == 'a' else 'desc'} nulls last")

        tools = cur.fetchall()

        print(
            f'Your tools ({"category" if by == "c" else "name"} {"ascending" if ord == "a" else "descending"}):')
        for tool in tools:
            show_tool(cur, username, tool)
    except:
        return False

    return True
