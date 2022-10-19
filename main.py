from psycopg2 import connect
from sshtunnel import SSHTunnelForwarder

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

                succ, e_constraint = create_user(
                    conn, username, password, first_name, last_name, email)
                if succ:
                    print('Created successfully')
                    logged_in = True
                elif e_constraint == 'users_pkey':
                    print('Username already in use')
                elif e_constraint == 'users_email_key':
                    print('Email already in use')
                else:
                    print('Error on creation')
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
                    pass
                elif flags[0] == 'e':
                    pass
                elif flags[0] == 'd':
                    pass
            elif command == 'categ':
                if flags[0] == 'v':
                    pass
                elif flags[0] == 'a':
                    pass
                elif flags[0] == 'e':
                    pass
                elif flags[0] == 'd':
                    pass
            elif command == 'reqs':
                if flags[0] == 'g':
                    pass
                elif flags[0] == 'r':
                    pass
            elif command == 'search':
                pass

        print('Thanks for trusting Mvie Lovers!')


if __name__ == '__main__':
    main()
