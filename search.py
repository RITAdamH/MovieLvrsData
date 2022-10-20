from psycopg2.extensions import cursor

from tools import show_tool


def search_tools(cur: cursor, username: str, barcode: str, name: str, categ: str) -> bool:
    try:
        # TODO: maybe refactor
        if categ:
            cur.execute(
                f"select * from tools where barcode like '%{barcode}%' and name like '%{name}%' and barcode in (select barcode from tool_categs where cid in (select cid from categories where username = '{username}' and name like '%{categ}%'))")
        else:
            cur.execute(
                f"select * from tools where barcode like '%{barcode}%' and name like '%{name}%'")

        tools = cur.fetchall()

        print(f'Found {len(tools)} tools:')
        for tool in tools:
            show_tool(tool)
    except:
        return False

    return True
