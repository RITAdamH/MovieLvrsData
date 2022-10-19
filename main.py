from psycopg2 import connect
from sshtunnel import SSHTunnelForwarder

from categories import (add_categ_tool, create_categ, delete_categ,
                        delete_categ_tool, edit_categ_name, show_categs)
from login import create_user, login_user
from tools import show_tools

COMMAND_FLAGS = {
    'help': (),
    'quit': (),
    'tool': ('v', 'a', 'e', 'd'),
    'categ': ('v', 'a', 'e', 'd'),
    'reqs': ('g', 'r'),
    'search': ()
}


def main() -> None:
    username = 'prj7465'
    password = 'lintThespian@1'
    dbName = 'p32001_17'

    with SSHTunnelForwarder(('starbug.cs.rit.edu', 22),
                            ssh_username=username,
                            ssh_password=password,
                            remote_bind_address=('localhost', 5432)) as server:
        server.start()
        print("SSH tunnel established")
        params = {
            'autocommit': True,
            'database': dbName,
            'user': username,
            'password': password,
            'host': 'localhost',
            'port': server.local_bind_port,
        }

        conn = connect(**params)
        print("Database connection established")
        logged_in = False

        while not logged_in:
            print('Welcome to MvieLvrs tools application')
            inp = input(
                'Enter "login" to login, "new" to create an account, or "quit" to quit: ').lower()
            if inp == 'login':
                print('Logging in')
                username = input('Username: ')
                password = input('Password: ')
                res = login_user(conn, username, password)
                if res is None:
                    print('Error logging in')
                elif res:
                    print('Login successful')
                    logged_in = True
                else:
                    print('Incorrect login')
            elif inp == 'new':
                print('Creating user')
                username = input('Username: ')
                if not username:
                    print('Username cannot be empty')
                    continue
                password = input('Password: ')
                if not password:
                    print('Password cannot be empty')
                    continue
                first_name = input('First Name: ')
                if not first_name:
                    print('First Name cannot be empty')
                    continue
                last_name = input('Last Name: ')
                if not last_name:
                    print('Last Name cannot be empty')
                    continue
                email = input('Email: ')
                if not email:
                    print('Email cannot be empty')
                    continue

                res = create_user(conn, username, password,
                                  first_name, last_name, email)
                if res is None:
                    print('Error creating user')
                elif res:
                    print('User created')
                else:
                    print('Username or email already exists')
            elif inp == 'quit':
                break
            else:
                print('Unrecognized input')

        if logged_in:
            print('You are now logged in')

        while logged_in:
            print('Enter a command ("help" for help, "quit" to quit)')
            inp = input('> ').lower()
            command, *flags = inp.split()
            if command not in COMMAND_FLAGS:
                print('Unknown command - see "help"')
            elif bool(flags) != bool(COMMAND_FLAGS[command]) or flags and flags[0] not in COMMAND_FLAGS[command]:
                print('Invalid usage - see "help"')
            elif command == 'help':
                print('Commands:')
                print('help             -  displays this menu')
                print('quit             -  exits the program')
                print(
                    'tool [v a e d]   -  manage your tools [view add edit delete]')
                print(
                    'categ [v a e d]  -  manage your categories [view add edit delete]')
                print(
                    'reqs [g r]       -  manage your borrow requests [given recieved]')
                print('search           -  search for tool')
            elif command == 'quit':
                break
            elif command == 'tool':
                if flags[0] == 'v':
                    by = input('Sort by category or name? (c/n): ').lower()
                    if by in ('c', 'n'):
                        ord = input('Ascending or descending? (a/d): ').lower()
                        if ord in ('a', 'd'):
                            if not show_tools(conn, username, by, ord):
                                print('Error showing tools')
                        else:
                            print('Invalid input')
                    else:
                        print('Invalid input')
                elif flags[0] == 'a':
                    raise NotImplementedError
                elif flags[0] == 'e':
                    raise NotImplementedError
                elif flags[0] == 'd':
                    raise NotImplementedError
            elif command == 'categ':
                if flags[0] == 'v':
                    if not show_categs(conn, username):
                        print('Error showing categories')
                elif flags[0] == 'a':
                    name = input('Name of new category: ')
                    if not name:
                        print('Name cannot be empty')
                        continue
                    res = create_categ(conn, username, name)
                    if res is None:
                        print('Error creating category')
                    elif res:
                        print('Created successfully')
                    else:
                        print('Category already exists')
                elif flags[0] == 'e':
                    name = input('Name of category to edit: ')
                    inp = input('Edit name or tools (n/t): ').lower()
                    if inp == 'n':
                        new_name = input('New name: ')
                        if not new_name:
                            print('Name cannot be empty')
                            continue
                        res = edit_categ_name(
                            conn, username, name, new_name)
                        if res is None:
                            print('Error editing category name')
                        elif res:
                            print('Edited name successfully')
                        else:
                            print('Category does not exist')
                    elif inp == 't':
                        inp = input('Add or remove tool (a/r): ').lower()
                        if inp == 'a':
                            tool_barcode = input('Tool barcode (must own): ')
                            res = add_categ_tool(
                                conn, username, name, tool_barcode)
                            if res is None:
                                print('Error adding tool to category')
                            elif res:
                                print('Added tool to category successfully')
                            else:
                                print(
                                    'Category or tool does not exist or tool is not owned or tool already is in category')
                        elif inp == 'r':
                            tool_barcode = input('Tool barcode: ')
                            res = delete_categ_tool(
                                conn, username, name, tool_barcode)
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
                    res = delete_categ(conn, username, name)
                    if res is None:
                        print('Error deleting category')
                    elif res:
                        print('Deleted successfully')
                    else:
                        print('Category does not exist')
            elif command == 'reqs':
                if flags[0] == 'g':
                    raise NotImplementedError
                elif flags[0] == 'r':
                    raise NotImplementedError
            elif command == 'search':
                raise NotImplementedError

        print('Thanks for trusting Mvie Lovers!')

        conn.close()


if __name__ == '__main__':
    main()
