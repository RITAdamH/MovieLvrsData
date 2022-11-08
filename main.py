"""
filename: main.py
Author: Brett Lubberts (bpl991), Connor Stange (cjs5232), Jose Estevez (jae9307),
        Adam Harnish (afh9608), Patrick Johnson (prj7465)
Description: Implementation for a Python interface so that users may interact with a Starbug database of tools.
"""


from configparser import ConfigParser
from psycopg2 import connect
from sshtunnel import SSHTunnelForwarder
from categories import add_categ_tool, create_categ, delete_categ, delete_categ_tool, edit_categ_name, show_categs
from login import create_user, login_user
from requests import accept_req, create_req, delete_req, reject_req, show_reqs_given, show_reqs_received
from search import search_tools_barcode, search_tools_name_categ
from stats import show_dashboard, show_most_borrowed, show_most_lent
from tools import add_tool, edit_tool, remove_tool, return_tool, show_tools_available, show_tools_borrowed, show_tools_lent, show_tools_owned

COMMAND_FLAGS = {
    'help': (),
    'quit': (),
    'tool': ('v', 'a', 'e', 'd', 'r', 's'),
    'categ': ('v', 'c', 'e', 'd'),
    'req': ('g', 'r'),
    'stat': ('d', 'l', 'b')
}

DB_NAME = 'p32001_17'


"""
main engine for the program
@return None
"""


def main() -> None:
    config = ConfigParser()
    config.read('ssh.ini')
    if config.has_option('ssh', 'username') and config.has_option('ssh', 'password'):
        ssh_username = config['ssh']['username']
        ssh_password = config['ssh']['password']
    else:
        print('No valid ssh.ini found, please enter credentials')
        ssh_username = input('SSH username: ')
        ssh_password = input('SSH password: ')

    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=ssh_username,
                            ssh_password=ssh_password,
                            remote_bind_address=('localhost', 5432)) as server:
        server.start()
        print('SSH tunnel established')
        con = connect(database=DB_NAME, user=ssh_username, password=ssh_password,
                      host='localhost', port=server.local_bind_port)
        print('Database connection established')
        con.autocommit = True
        cur = con.cursor()

        logged_in = False

        while not logged_in:
            print('Welcome to MvieLovers tools application')
            inp = input(
                'Enter "login" to login, "new" to create an account, or "quit" to quit: ').lower().strip()
            if inp == 'login':
                username = input('Username: ')
                password = input('Password: ')
                res = login_user(cur, username, password)
                if res is None:
                    print('Error logging in')
                elif res:
                    print('Login successful')
                    logged_in = True
                else:
                    print('Invalid login credentials')
            elif inp == 'new':
                print('Creating user')
                username = input('Username: ')
                password = input('Password: ')
                first_name = input('First Name: ')
                last_name = input('Last Name: ')
                email = input('Email: ')
                res = create_user(cur, username, password,
                                  first_name, last_name, email)
                if res is None:
                    print('Error creating user')
                elif res:
                    print('User created successfully')
                    logged_in = True
                else:
                    print('Username or email already exists')
            elif inp == 'quit':
                break
            else:
                print('Unrecognized input')

        while logged_in:
            print('Enter a command ("help" for help, "quit" to quit)')
            inp = input('> ').lower().strip()
            command, *flags = inp.split()
            if command not in COMMAND_FLAGS:
                print('Unknown command - see "help"')
            elif len(flags) > 1 or bool(flags) != bool(COMMAND_FLAGS[command]) or flags and flags[0] not in COMMAND_FLAGS[command]:
                print('Invalid usage - see "help"')
            elif command == 'help':
                print('Commands:')
                print('help                -  displays this menu')
                print('quit                -  exits the program')
                print(
                    'tool [v a e d r s]  -  manage your tools [view add edit delete return search]')
                print(
                    'categ [v c e d]     -  manage your categories [view create edit delete]')
                print(
                    'req [g r]           -  manage your borrow requests [given received]')
                print(
                    'stat [d l b]       -  show statistics [dashboard lent borrowed]')
            elif command == 'quit':
                break
            elif command == 'tool':
                if flags[0] == 'v':
                    inp = input(
                        'Show all owned, all borrowed, all lent, or all available tools? (o/b/l/a): ').lower().strip()
                    if inp == 'o':
                        by = input(
                            'Sort by category or name? (c/n): ').lower().strip()
                        if by in ('c', 'n'):
                            ord = input(
                                'Ascending or descending? (a/d): ').lower().strip()
                            if ord in ('a', 'd'):
                                if not show_tools_owned(cur, username, by, ord):
                                    print('Error showing tools')
                            else:
                                print('Invalid input')
                        else:
                            print('Invalid input')
                    elif inp == 'b':
                        if not show_tools_borrowed(cur, username):
                            print('Error showing tools')
                    elif inp == 'l':
                        if not show_tools_lent(cur, username):
                            print('Error showing tools')
                    elif inp == 'a':
                        if not show_tools_available(cur, username):
                            print('Error showing tools')
                    else:
                        print('Invalid input')
                elif flags[0] == 'a':
                    barcode = input('Barcode: ')
                    res = add_tool(cur, username, barcode)
                    if res is None:
                        print('Error adding tool')
                    elif res:
                        print('Tool added')
                    else:
                        print('Tool is already owned, or does not exist')
                elif flags[0] == 'e':
                    barcode = input('Barcode: ')
                    shareable = input(
                        'Make shareable? (y/n): ').lower().strip()
                    if shareable in ('y', 'n'):
                        res = edit_tool(cur, username, barcode,
                                        shareable == 'y')
                        if res is None:
                            print('Error editing tool')
                        elif res:
                            print('Tool edited')
                        else:
                            print('Tool is not owned by you, or does not exist')
                    else:
                        print('Invalid input')
                elif flags[0] == 'd':
                    barcode = input('Barcode: ')
                    res = remove_tool(cur, username, barcode)
                    if res is None:
                        print('Error deleting tool')
                    elif res:
                        print('Tool deleted')
                    else:
                        print(
                            'Tool is not owned by you, or does not exist, or is lent out')
                elif flags[0] == 'r':
                    barcode = input('Barcode: ')
                    res = return_tool(cur, username, barcode)
                    if res is None:
                        print('Error returning tool')
                    elif res:
                        print('Tool returned')
                    else:
                        print('Tool is not borrowed by you, or does not exist')
                elif flags[0] == 's':
                    barcode = input('Tool barcode (enter to omit): ')
                    if barcode:
                        if not search_tools_barcode(cur, username, barcode):
                            print('Error searching for tools')
                    else:
                        name = input('Tool name (enter to omit): ').lower()
                        categ = input(
                            'Tool category (enter to omit): ').lower()
                        if not search_tools_name_categ(cur, username, name, categ):
                            print('Error searching for tools')
            elif command == 'categ':
                if flags[0] == 'v':
                    if not show_categs(cur, username):
                        print('Error showing categories')
                elif flags[0] == 'c':
                    name = input('Name of new category: ')
                    res = create_categ(cur, username, name)
                    if res is None:
                        print('Error creating category')
                    elif res:
                        print('Created successfully')
                    else:
                        print('Category already exists')
                elif flags[0] == 'e':
                    name = input('Name of category to edit: ')
                    inp = input('Edit name or tools (n/t): ').lower().strip()
                    if inp == 'n':
                        new_name = input('New name: ')
                        res = edit_categ_name(
                            cur, username, name, new_name)
                        if res is None:
                            print('Error editing category name')
                        elif res:
                            print('Edited name successfully')
                        else:
                            print(
                                'Category does not exist or name is already in use')
                    elif inp == 't':
                        inp = input(
                            'Add or remove tool (a/r): ').lower().strip()
                        if inp == 'a':
                            tool_barcode = input('Tool barcode (must own): ')
                            res = add_categ_tool(
                                cur, username, name, tool_barcode)
                            if res is None:
                                print('Error adding tool to category')
                            elif res:
                                print('Added tool to category successfully')
                            else:
                                print(
                                    'Category or tool does not exist or tool is not owned or tool already is in '
                                    'category')
                        elif inp == 'r':
                            tool_barcode = input('Tool barcode: ')
                            res = delete_categ_tool(
                                cur, username, name, tool_barcode)
                            if res is None:
                                print('Error removing tool from category')
                            elif res:
                                print('Removed tool from category successfully')
                            else:
                                print('Category or tool does not exist')
                        else:
                            print('Invalid input')
                    else:
                        print('Invalid input')
                elif flags[0] == 'd':
                    name = input('Name of category to delete: ')
                    res = delete_categ(cur, username, name)
                    if res is None:
                        print('Error deleting category')
                    elif res:
                        print('Category deleted successfully')
                    else:
                        print('Category does not exist')
            elif command == 'req':
                if flags[0] == 'g':
                    inp = input(
                        'View, create or delete requests (v/c/d): ').lower().strip()
                    if inp == 'v':
                        if not show_reqs_given(cur, username):
                            print('Error showing requests')
                    elif inp == 'c':
                        barcode = input('Tool barcode: ')
                        date_required = input('Date tools is required: ')
                        duration = input('Duration: ')
                        res = create_req(cur, username, barcode,
                                         date_required, duration)
                        if res is None:
                            print('Error creating request')
                        elif res:
                            print('Request created successfully')
                        else:
                            print(
                                'Tool does not exist or is owned by you or is not owned or is not shareable or is '
                                'already lent out or is recently requested by you or duration is not long enough')
                    elif inp == 'd':
                        barcode = input('Tool barcode: ')
                        request_date = input('Request date: ')
                        res = delete_req(cur, username, barcode, request_date)
                        if res is None:
                            print('Error deleting request')
                        elif res:
                            print('Request deleted successfully')
                        else:
                            print(
                                'Request does not exist or is not made by you or is not pending')
                    else:
                        print('Invalid input')
                elif flags[0] == 'r':
                    inp = input(
                        'View or resolve requests (v/r): ').lower().strip()
                    if inp == 'v':
                        if not show_reqs_received(cur, username):
                            print('Error showing requests')
                    elif inp == 'r':
                        req_username = input('User requesting: ')
                        barcode = input('Tool barcode: ')
                        request_date = input('Request date: ')
                        decision = input(
                            'Accept or reject (a/r): ').lower().strip()
                        if decision == 'a':
                            expected_return_date = input(
                                'Expected return date: ')
                            res = accept_req(
                                cur, username, req_username, barcode, request_date, expected_return_date)
                            if res is None:
                                print('Error accepting request')
                            elif res:
                                print('Request accepted successfully')
                            else:
                                print(
                                    'Request does not exist or is not pending or is not to you or tool is not '
                                    'shareable or return date is too soon')
                        elif decision == 'r':
                            res = reject_req(
                                cur, username, req_username, barcode, request_date)
                            if res is None:
                                print('Error rejecting request')
                            elif res:
                                print('Request rejected successfully')
                            else:
                                print(
                                    'Request does not exist or is not pending or is not to you')
                        else:
                            print('Invalid input')
                    else:
                        print('Invalid input')
            elif command == 'stat':
                if flags[0] == 'd':
                    if not show_dashboard(cur, username):
                        print('Error showing dashboard')
                elif flags[0] == 'l':
                    if not show_most_lent(cur, username):
                        print('Error showing most lent tools')
                elif flags[0] == 'b':
                    if not show_most_borrowed(cur, username):
                        print('Error showing most borrowed tools')

        print('Thanks for trusting Mvie Lovers!')
        con.close()


if __name__ == '__main__':
    main()
