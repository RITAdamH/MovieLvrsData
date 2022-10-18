# Patrick

def main():
  conn = get_conn()  # TODO
  
  logged_in = False
  
  while not logged_in:
    print('Welcome to MvieLvrs tools application')
    inp = input('Enter l to login or c to create an account: ').lower()
    if inp == 'l':
      print('Log in')
      username = input('Username: ')
      password = input('Password: ')
      if login_user(conn, username, password):
        print('Login successful')
        logged_in = True
        break
      else:
        print('Incorrect login')
    elif inp == 'c':
      print('Creating user')
      if create_user(conn, username, password, first_name, last_name, email):
        print('Created successfully')
        logged_in = True
        break
      else:
        print('Error on creation')
    else:
      print('Unrecognized input')
  
  print('You are now logged in')
  inp = input('Enter a command (h for help)').lower()
  
