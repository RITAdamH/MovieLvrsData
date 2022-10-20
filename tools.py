from typing import Any

from psycopg2.extensions import cursor


def show_tool(tool: tuple[Any], categs: list[str] | None = None) -> None:
    print(f'{tool[1]} [{tool[0]}]')
    print(f'"{tool[2]}"')
    print(f'Purchased on {tool[3]} (${tool[4]:.2f})')
    print(f'{"Shareable" if tool[5] else "Not shareable"}')
    if categs is not None:
        print(f'Categories: {", ".join(categs)}')
    print()


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
            cur.execute(
                f"select name from categories where username = '{username}' and cid in (select cid from tool_categs where barcode = '{tool[0]}') order by name asc")

            categs = cur.fetchall()

            show_tool(tool, [categ[0] for categ in categs])
    except:
        return False

    return True
