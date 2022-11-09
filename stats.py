from psycopg2.extensions import cursor

from tools import show_tool


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


def show_most_borrowed(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"select tools.*, sum(coalesce(date_returned, current_date) - last_status_change + 1) as days_borrowed from tools, tool_reqs where tools.barcode = tool_reqs.barcode and tool_reqs.username = '{username}' and tool_reqs.status = 'Accepted' group by tools.barcode order by days_borrowed desc, name, barcode limit 10")

        tools_borrowed_stats = cur.fetchall()

        if not tools_borrowed_stats:
            print('You have no borrow stats to show')
        else:
            print(
                f'Your top ({len(tools_borrowed_stats)}) most borrowed tools [days borrowed descending]:')
            for i, tool_borrowed_stats in enumerate(tools_borrowed_stats):
                *tool, days_borrowed = tool_borrowed_stats
                print(
                    f'#{i + 1}. {days_borrowed} day(s)')
                show_tool(cur, username, tool)
    except:
        return False

    return True


def show_most_lent(cur: cursor, username: str) -> bool:
    try:
        cur.execute(
            f"with tools_lent_stats as (select tools.*, sum(coalesce(date_returned, current_date) - last_status_change + 1) as days_lent, current_date - tools.purchase_date as days_owned, avg(coalesce(date_returned, current_date) - last_status_change + 1)::numeric as avg_days_lent from tools, tool_reqs where tools.barcode = tool_reqs.barcode and tools.username = '{username}' and tool_reqs.status = 'Accepted' group by tools.barcode) select *, days_lent::numeric / days_owned as lent_pct from tools_lent_stats order by lent_pct desc, name, barcode limit 10")

        tools_lent_stats = cur.fetchall()

        if not tools_lent_stats:
            print('You have no lend stats to show')
        else:
            print(
                f'Your top ({len(tools_lent_stats)}) most lent tools [percentage lent descending]:')
            for i, tool_lent_stats in enumerate(tools_lent_stats):
                *tool, days_lent, days_owned, avg_days_lent, lent_pct = tool_lent_stats
                print(
                    f'#{i + 1}. {lent_pct:.2%} - lent for {days_lent}/{days_owned} day(s) ({avg_days_lent:.2f} day(s) avg.)')
                show_tool(cur, username, tool)
    except:
        return False

    return True
