from psycopg2.extensions import connection


def show_tools(conn: connection, username: str, by: str, ord: str) -> bool:
    cursr = conn.cursor()

    try:
        if by == 'n':
            cursr.execute(
                f"select * from tools where username = '{username}' order by name {'asc' if ord == 'a' else 'desc'}")
        else:
            raise NotImplementedError  # TODO add sort by category

        tools = cursr.fetchall()

        print(
            f'Your tools ({"category" if by == "c" else "name"} {"ascending" if ord == "a" else "descending"}):')
        for tool in tools:
            print(f'{tool[1]} [{tool[0]}]')
            print(f'"{tool[2]}"')
            print(f'Purchased on {tool[3]} (${tool[4]:.2f})')
            print(f'{"Shareable" if tool[5] else "Not shareable"}')
            print()
    except:
        return False

    return True
