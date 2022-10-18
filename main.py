# Patrick

def main():
  conn = get_conn()  # TODO
  
  logged_in = False
  
  while not logged_in:
    print('Welcome to MvieLvrs tools application')
    inp = input('Enter "login" to login or "new" to create an account: ').lower()
    if inp == 'login':
      print('Logging in')
      username = input('Username: ')
      password = input('Password: ')
      if login_user(conn, username, password):
        print('Login successful')
        logged_in = True
      else:
        print('Incorrect login')
    elif inp == 'new':
      print('Creating user')
      username = input('Username: ')
      password = input('Password: ')
      first_name = input('First Name: ')
      last_name = input('Last Name: ')
      email = input('Email: ')
      if create_user(conn, username, password, first_name, last_name, email):
        print('Created successfully')
        logged_in = True
      else:
        print('Error on creation')
    else:
      print('Unrecognized input')
  
  print('You are now logged in')
  while True:
    inp = input('Enter a command ("help" for help)').lower()
    command, *flags = inp.split()
    if command not in FLAGS or len(FLAGS_DICT[command])
    if command == 'help':
      if flags:
        print('No flags needed for this command')
      else:
        print('Commands:')
        print('help             -  displays this menu')
        print('quit             -  exits the program')
        print('tool [v a e d]   -  manage tools [view add edit delete]')
        print('categ [v a e d]  -  manage categories [view add edit delete]')
        print('search [b n c]   -  search for tool [barcode name category]')
        print('borrow           -  borrow a tool')
        print('reqs [g r]       -  manage borrow requests [given recieved]')
        print('return           -  return a borrowed tool')
    elif inp == 'quit':
      if flags:
        print('No flags needed for this command')
      else:
        break
  
  print('Thanks for trusting Mvie Lovers!')

if __name__ == '__main__':
  main()
