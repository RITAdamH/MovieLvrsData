from psycopg2.extensions import cursor


def show_dashboard(cur: cursor, username: str) -> bool:
    try:
        print('Your dashboard')
        print('-' * 50)

        cur.execute(
            f"select * from tools where username = '{username}' and barcode not in (select barcode from tool_reqs where status != 'Accepted' or date_returned is not null)")

        print(f'Tools available from catalog: {cur.rowcount}')

        cur.execute(
            f"select tools.* from tools, tool_reqs where tools.barcode = tool_reqs.barcode and tools.username = '{username}' and tool_reqs.status = 'Accepted' and tool_reqs.date_returned is null")

        print(f'Tools lent: {cur.rowcount}')

        cur.execute(
            f"select tools.* from tools, tool_reqs where tools.barcode = tool_reqs.barcode and tool_reqs.username = '{username}' and tool_reqs.status = 'Accepted' and tool_reqs.date_returned is null")

        print(f'Tools borrowed: {cur.rowcount}')

        print('-' * 50)
    except:
        return False

    return True
