"""
filename: search.py
Author: Patrick Johnson & Connor Stange
Description: File containing any functions that query the database to search for a tool given a barcode,
             name, or category
"""


from psycopg2.extensions import cursor
from tools import show_tool


"""
search tools using a specified "barcode format"
@param cur: the cursor to the database
@param username: the users username
@param barcode: the barcode to be searched
@return True if execution successful (prints outcome), False if error
"""


def search_tools_barcode(cur: cursor, username: str, barcode: str) -> bool:
    try:
        cur.execute(
            f"select * from tools where barcode = '{barcode}'")

        tool = cur.fetchone()

        if tool is None:
            print('No tool has that barcode')
        else:
            print('Found a tool with that barcode:')
            show_tool(cur, username, tool)
    except:
        return False

    return True


"""
search tools using a standard name and category format
@param cur: the cursor to the database
@param username: the users username
@param barcode: the name or category
@return True if executions are successful (prints outcome), False if error
"""


def search_tools_name_categ(cur: cursor, username: str, name: str, categ: str) -> bool:
    try:
        if categ:
            cur.execute(
                f"select * from tools where lower(name) like '%{name}%' and barcode in (select barcode from "
                f"tool_categs where cid in (select cid from categories where username = '{username}' and lower(name) "
                f"like '%{categ}%')) order by name asc")
        else:
            cur.execute(
                f"select * from tools where lower(name) like '%{name}%' order by name asc")

        tools = cur.fetchall()

        if not tools:
            print('No tools found matching criteria')
        else:
            print(f'Found {len(tools)} tool(s) matching criteria:')
            for tool in tools:
                show_tool(cur, username, tool)
    except:
        return False

    return True
